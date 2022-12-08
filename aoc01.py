import sys

l = [0]
for line in sys.stdin.readlines():
  if not line.strip():
    l.append(0)
    continue
  l[-1] += int(line.strip())

l.sort()
print('\n'.join(str(n) for n in l))
print(sum(l[-3:]))
