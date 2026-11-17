# HashCrack

HashCrack is a command-line password hash cracker written in Python, built for lab and learning use. It takes a file of password hashes and a wordlist, and tries to recover the original passwords.

## Features

- Automatic hash-type detection (MD5, SHA-1, SHA-256) from the hash length and format
- Dictionary attack using Python's built-in hashlib
- Optional rule-based mutations: upper / lower / capitalized forms, leet-speak substitutions, and appended digits and years (1, 12, 123, 1234, !, 2023-2026)
- Salted-hash support in salt:hash format - both salt+password and password+salt orderings are tried
- Multi-hash input: many hashes cracked in a single run, and cracked targets are removed from the working set
- Live progress display, plus a report file with the results and the total run time

## Requirements

- Python 3 (no extra libraries needed - only the Python standard library)

## How to run

    py HashCrack.py --hashes test_hashes.txt --wordlist wordlist.txt --rules

(On a system where the `python` command works directly, use `python` instead of `py`.)

Options:
- `--hashes` : file with target hashes, one per line (required)
- `--wordlist` : wordlist file, one word per line (required)
- `--rules` : turn ON word mutations (optional)
- `--report` : report file name (optional, default is report.txt)

Without `--rules`, only the raw wordlist words are tried. With `--rules`, every word is also tried in its mutated forms.

## Example result

With rules ON, 5 of 6 lab hashes were cracked (hello, dragon, python, Dragon123, and a salted dragon). With rules OFF, only 4 of 6 were cracked - the mutated password Dragon123 was missed, which shows why the rules engine matters.

## Lab use only

This tool was built for a coursework lab. It must only be used on hashes you created yourself for learning. Never use it on real or leaked password hashes.

## Author

Umer - PNY Trainings, Cyber Security Department
Final Project: Cryptography and Password Attacks
