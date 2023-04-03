import calendar

class A:
    pass

m = calendar.month(2023, 4)
print("Calendar\n========")
sep = '+' + '+'.join(['--']*7) + '+'
lines = m.split('\n')
A.h = len(lines) - 1
A.w = len(lines[1])
for n, l in enumerate(lines):
    days = l.split()
    match n:
        case 0:
            print(f'+{"-"*A.w}+')
            print(f'|{l:{A.w}}|')
        case 2:
            print(sep)
            days = (7 - len(days)) * [""] + days
            print("|"+"|".join(f"{s:2}" for s in days) + "|")
        case A.h:
            print(sep)
        case _:
            print(sep)
            days = (days + "       ".split(" "))[:7]
            print("|"+"|".join(f"{s:2}" for s in days) + "|")
