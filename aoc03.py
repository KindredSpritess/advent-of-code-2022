import sys

s = 0
cs = [chr(a) for a in range(ord('a'), ord('z')+1)] + [chr(a) for a in range(ord('A'), ord('Z')+1)]
priority = {a: i for i, a in enumerate(cs)}
lines = sys.stdin.readlines()
it = iter(lines)
for ls in zip(it, it, it):
  a, b, c = (set(l.strip()) for l in ls)
  c = a & b & c
  assert len(c) == 1
  s += priority[c.pop()] + 1

print(s)
