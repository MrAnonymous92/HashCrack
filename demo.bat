@echo off
cd /d %~dp0
echo ===== RUN 1: RULES ON =====
py HashCrack.py --hashes test_hashes.txt --wordlist wordlist.txt --rules
echo.
echo ===== RUN 2: RULES OFF =====
py HashCrack.py --hashes test_hashes.txt --wordlist wordlist.txt --report report2.txt
echo.
echo Demo khatam. Band karne ke liye koi bhi key dabayen.
pause

