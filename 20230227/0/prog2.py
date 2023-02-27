import shlex

name = input()
pl = input()

print(s := shlex.join(['register', name, pl]))
print(shlex.split(s))


