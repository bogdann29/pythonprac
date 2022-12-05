import sys

buf = sys.stdin.buffer.read()

N = buf[0]
L = len(buf[1:])
buf1 = buf[1:]

res = []
for i in range(N+1):
    ln = int((i+1)*L/N) - int(i*L/N)
    if ln != 0:
        res.append(buf1[int(i*L/N): int((i+1)*L/N)])
res.sort()
ans = b"" + buf[:1]
for c in res:
    ans += c
sys.stdout.buffer.write(ans)