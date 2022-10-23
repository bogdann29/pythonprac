s = input().lower()
print(len(set([s[i:i+2] for i in range(len(s)-1) if s[i].isalpha() and s[i+1].isalpha()])))