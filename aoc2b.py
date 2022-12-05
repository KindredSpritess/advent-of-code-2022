import sys

s = 0
cs = {'X': 0, 'Y': 1, 'Z': 2}
ts = {'A': 0, 'B': 1, 'C': 2}
for line in sys.stdin.readlines():
  o, m = line.strip().split()
  o = ts[o]
  if m == 'X':
    m = (o - 1) % 3
  elif m == 'Y':
    m = o
  else:
    m = (o + 1) % 3
  s += m + 1
  s += (m == o) * 3
  s += 6 * (((m - 1) % 3) == o)

print(s)
