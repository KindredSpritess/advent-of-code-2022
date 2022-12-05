import sys

s = 0
cs = {'X': 0, 'Y': 1, 'Z': 2}
ts = {'A': 0, 'B': 1, 'C': 2}
for line in sys.stdin.readlines():
  o, m = line.strip().split()
  s += cs[m] + 1
  s += (cs[m] == ts[o]) * 3
  s += 6 * (((cs[m] - 1) % 3) == ts[o])

print(s)
