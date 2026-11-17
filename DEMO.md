# HashCrack - Demo Write-up

## Test setup

- Wordlist (wordlist.txt): 5 words - hello, computer, dragon, python, hacker
- Target file (test_hashes.txt): 6 hashes I generated myself in the lab:
  1. MD5 of hello
  2. SHA-256 of dragon
  3. SHA-1 of python
  4. MD5 of Dragon123 (a mutated password - not in the wordlist)
  5. Salted MD5 in salt:hash format (salt xyz + dragon)
  6. MD5 of zebra (deliberately not in the wordlist)

## Runs

Run 1 (rules ON):
    py HashCrack.py --hashes test_hashes.txt --wordlist wordlist.txt --rules
Result: Cracked 5/6. Report saved to report.txt.

Run 2 (rules OFF):
    py HashCrack.py --hashes test_hashes.txt --wordlist wordlist.txt --report report2.txt
Result: Cracked 4/6.

## One cracked result, explained

The target 0a76ac0b32c1f99c6a1aca630b01ed81 was cracked as Dragon123, and only when rules were ON.
The wordlist contains only dragon. The rules engine first applied the Capitalize rule
(dragon -> Dragon) and then the appended-digits rule (Dragon + 123 -> Dragon123).
The MD5 of Dragon123 matched the target, so the password was recovered.
With rules OFF, the same hash stayed in the NOT CRACKED list - this is the proof that the rules engine works.

The only uncracked hash was the MD5 of zebra, which is correct behaviour,
because zebra is not in the wordlist and no mutation of a wordlist word produces it.
