import sys

print(sys.stdin.read().encode('latin1', errors = 'replace').decode('CP1251', errors = 'replace'))
