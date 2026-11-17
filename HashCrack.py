import argparse
import hashlib
import time

LEET = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$", "t": "7"}


def detect_hash(h):
    h = h.strip().lower()
    if all(c in "0123456789abcdef" for c in h):
        if len(h) == 32:
            return "md5"
        if len(h) == 40:
            return "sha1"
        if len(h) == 64:
            return "sha256"
    return "unknown"


def leet(word):
    result = ""
    for ch in word:
        result += LEET.get(ch.lower(), ch)
    return result


def mutations(word):
    seen = set()
    results = []

    def add(w):
        if w not in seen:
            seen.add(w)
            results.append(w)

    add(word)
    add(word.lower())
    add(word.upper())
    add(word.capitalize())
    add(leet(word))

    for suffix in ["1", "12", "123", "1234", "!", "2023", "2024", "2025", "2026"]:
        add(word + suffix)
        add(word.capitalize() + suffix)

    return results


def make_hash(text, algo):
    h = hashlib.new(algo)
    h.update(text.encode())
    return h.hexdigest()


def load_targets(filename):
    targets = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                salt, hexhash = line.split(":", 1)
            else:
                salt, hexhash = None, line
            algo = detect_hash(hexhash)
            if algo == "unknown":
                print("Unknown hash format, skipped:", line)
                continue
            targets[line] = (salt, hexhash.lower(), algo)
    return targets


def main():
    parser = argparse.ArgumentParser(description="HashCrack - hash password cracker (lab use only)")
    parser.add_argument("--hashes", required=True, help="File with target hashes, one per line")
    parser.add_argument("--wordlist", required=True, help="Wordlist file")
    parser.add_argument("--rules", action="store_true", help="Turn ON word mutations")
    parser.add_argument("--report", default="report.txt", help="Report file name")
    args = parser.parse_args()

    targets = load_targets(args.hashes)
    total = len(targets)
    print(f"Loaded {total} target hashes. Rules: {'ON' if args.rules else 'OFF'}")

    with open(args.wordlist) as f:
        words = [line.strip() for line in f if line.strip()]

    cracked = {}
    tried = 0
    start = time.time()

    for i, word in enumerate(words, start=1):
        if not targets:
            break
        candidates = mutations(word) if args.rules else [word]
        for cand in candidates:
            if not targets:
                break
            tried += 1
            for line in list(targets.keys()):
                salt, hexhash, algo = targets[line]
                if salt is None:
                    tries = [cand]
                else:
                    tries = [salt + cand, cand + salt]
                for t in tries:
                    if make_hash(t, algo) == hexhash:
                        cracked[line] = cand if salt is None else word
                        del targets[line]
                        print(f"Cracked: {line} -> password: {cracked[line]}")
                        break
        print(f"Progress: word {i}/{len(words)}, {tried} candidates tried, {len(cracked)}/{total} cracked")

    elapsed = time.time() - start

    print()
    print(f"Done in {elapsed:.2f} seconds. Cracked {len(cracked)}/{total}.")

    with open(args.report, "w") as r:
        r.write("HashCrack Report\n")
        r.write("================\n")
        r.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        r.write(f"Wordlist: {args.wordlist}\n")
        r.write(f"Rules: {'ON' if args.rules else 'OFF'}\n")
        r.write(f"Total time: {elapsed:.2f} seconds\n\n")
        r.write(f"CRACKED ({len(cracked)}):\n")
        for line, pw in cracked.items():
            r.write(f"{line} = {pw}\n")
        r.write(f"\nNOT CRACKED ({len(targets)}):\n")
        for line in targets:
            r.write(f"{line}\n")

    print(f"Report saved to {args.report}")


if __name__ == "__main__":
    main()
