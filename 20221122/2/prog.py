import sys

print(sys.stdin.read().encode('latin1').decode('CP1251', errors = 'replace'))