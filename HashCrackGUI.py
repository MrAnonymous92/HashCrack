# ============================================
# HashCrack GUI - Password Hash Cracker
# Graphical version of HashCrack (PNY Trainings Final Project)
# Engine is the same as HashCrack.py - only the interface is new.
# ============================================

import hashlib
import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

BASE = os.path.dirname(os.path.abspath(__file__))


# ---------------- Engine (same as CLI version) ----------------

def detect_hash(h):
    """Hash ki type us ki lambai se pehchano: md5 / sha1 / sha256."""
    h = h.strip().lower()
    hexdigits = "0123456789abcdef"
    if len(h) == 32 and all(c in hexdigits for c in h):
        return "md5"
    if len(h) == 40 and all(c in hexdigits for c in h):
        return "sha1"
    if len(h) == 64 and all(c in hexdigits for c in h):
        return "sha256"
    return None


def make_hash(algo, text):
    return hashlib.new(algo, text.encode()).hexdigest()


def leet(word):
    table = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$"}
    return "".join(table.get(c, c) for c in word)


def mutations(word):
    """Ek word ki saari shaklein (rules): 22 forms."""
    forms = []
    for b in [word, word.upper(), word.capitalize(), leet(word)]:
        if b not in forms:
            forms.append(b)
    suffixes = ["1", "12", "123", "1234", "!", "2023", "2024", "2025", "2026"]
    for s in suffixes:
        for b in (word, word.capitalize()):
            f = b + s
            if f not in forms:
                forms.append(f)
    return forms


def crack_one(target_line, words, use_rules, progress_cb=None):
    """Ek hash crack karo. (password ya None, kitne try hue) return karta hai."""
    line = target_line.strip()
    salt = None
    target = line.lower()
    if ":" in line:
        salt, target = line.split(":", 1)
        target = target.strip().lower()
    algo = detect_hash(target)
    if algo is None:
        return None, 0
    tried = 0
    for w in words:
        candidates = mutations(w) if use_rules else [w]
        for cand in candidates:
            tried += 1
            if salt is not None:
                if make_hash(algo, salt + cand) == target:
                    return cand, tried
                if make_hash(algo, cand + salt) == target:
                    return cand, tried
            elif make_hash(algo, cand) == target:
                return cand, tried
        if progress_cb:
            progress_cb()
    return None, tried


# ---------------- GUI ----------------

class HashCrackApp:
    def __init__(self, root):
        self.root = root
        root.title("HashCrack - Password Hash Cracker")
        root.geometry("660x540")

        tk.Label(root, text="Hashes file:").grid(row=0, column=0, sticky="e", padx=8, pady=6)
        self.hashes_entry = tk.Entry(root, width=55)
        self.hashes_entry.insert(0, os.path.join(BASE, "test_hashes.txt"))
        self.hashes_entry.grid(row=0, column=1, padx=4, pady=6)
        tk.Button(root, text="Browse", command=lambda: self.browse(self.hashes_entry)).grid(row=0, column=2, padx=4)

        tk.Label(root, text="Wordlist file:").grid(row=1, column=0, sticky="e", padx=8, pady=6)
        self.wordlist_entry = tk.Entry(root, width=55)
        self.wordlist_entry.insert(0, os.path.join(BASE, "wordlist.txt"))
        self.wordlist_entry.grid(row=1, column=1, padx=4, pady=6)
        tk.Button(root, text="Browse", command=lambda: self.browse(self.wordlist_entry)).grid(row=1, column=2, padx=4)

        self.rules_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Rules ON (mutations - Capital, leet, numbers, years)",
                       variable=self.rules_var).grid(row=2, column=1, sticky="w", pady=4)

        self.start_btn = tk.Button(root, text="Start Cracking", width=20, command=self.start)
        self.start_btn.grid(row=3, column=1, pady=8)

        self.progress = ttk.Progressbar(root, length=520, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=3, padx=10, pady=4)
        self.status = tk.Label(root, text="Ready")
        self.status.grid(row=5, column=0, columnspan=3)

        self.output = ScrolledText(root, width=78, height=16, state="disabled")
        self.output.grid(row=6, column=0, columnspan=3, padx=10, pady=8)

        tk.Label(root, text="HashCrack GUI - by Umar Farooq").grid(row=7, column=0, columnspan=3, pady=2)

    def ui(self, func, *args):
        """Background thread se window ko safely update karne ke liye."""
        self.root.after(0, func, *args)

    def browse(self, entry):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def log(self, text):
        self.output.config(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.config(state="disabled")

    def start(self):
        hashes_file = self.hashes_entry.get().strip()
        wordlist_file = self.wordlist_entry.get().strip()
        if not os.path.isfile(hashes_file):
            messagebox.showerror("Error", "Hashes file nahi mili:\n" + hashes_file)
            return
        if not os.path.isfile(wordlist_file):
            messagebox.showerror("Error", "Wordlist file nahi mili:\n" + wordlist_file)
            return
        use_rules = self.rules_var.get()
        self.start_btn.config(state="disabled")
        self.progress.config(value=0)
        self.status.config(text="Cracking...")
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.config(state="disabled")
        thread = threading.Thread(target=self.run, args=(hashes_file, wordlist_file, use_rules), daemon=True)
        thread.start()

    def run(self, hashes_file, wordlist_file, use_rules):
        start_time = time.time()
        with open(wordlist_file, "r", encoding="utf-8", errors="ignore") as f:
            words = [line.strip() for line in f if line.strip()]
        with open(hashes_file, "r", encoding="utf-8", errors="ignore") as f:
            targets = [line.strip() for line in f if line.strip()]

        total_steps = max(len(words) * len(targets), 1)
        done = [0]

        def step():
            done[0] += 1
            pct = done[0] * 100 // total_steps
            self.ui(lambda: self.progress.config(value=pct))

        self.ui(self.log, f"Words: {len(words)}  |  Hashes: {len(targets)}  |  Rules: {'ON' if use_rules else 'OFF'}")
        self.ui(self.log, "-" * 60)

        cracked = []
        not_cracked = []
        for t in targets:
            pw, tried = crack_one(t, words, use_rules, step)
            if pw is not None:
                cracked.append((t, pw))
                self.ui(self.log, f"CRACKED:  {t}  =  {pw}")
            else:
                not_cracked.append(t)
                self.ui(self.log, f"NOT CRACKED:  {t}")

        elapsed = time.time() - start_time
        report_path = os.path.join(BASE, "report_gui.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("HashCrack GUI Report\n")
            f.write("====================\n")
            f.write(f"Rules: {'ON' if use_rules else 'OFF'}\n")
            f.write(f"Time taken: {elapsed:.2f} seconds\n\n")
            f.write(f"CRACKED ({len(cracked)}):\n")
            for h, pw in cracked:
                f.write(f"{h} = {pw}\n")
            f.write(f"\nNOT CRACKED ({len(not_cracked)}):\n")
            for h in not_cracked:
                f.write(f"{h}\n")

        self.ui(lambda: self.progress.config(value=100))
        self.ui(self.log, "-" * 60)
        self.ui(self.log, f"Done! Cracked {len(cracked)}/{len(targets)} in {elapsed:.2f} seconds")
        self.ui(self.log, f"Report saved: {report_path}")
        self.ui(lambda: self.status.config(text=f"Cracked {len(cracked)}/{len(targets)}"))
        self.ui(lambda: self.start_btn.config(state="normal"))


if __name__ == "__main__":
    root = tk.Tk()
    app = HashCrackApp(root)
    root.mainloop()
