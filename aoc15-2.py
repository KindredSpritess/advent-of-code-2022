import re
import sys
from collections import defaultdict

width = 4000001
#width = 21

def md(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)

ss = []
for line in sys.stdin.readlines():
  line = line.rstrip()
  sx, sy, bx, by = map(int, re.match(r'Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)', line).groups())
  ss.append((sx, sy, md(sx, sy, bx, by)))

x = y = 0
while x < width:
  y = 0
  while y < width:
    # should have some sort of trie structure to limit the sensors to affected rows
    for sx, sy, r in ss:
      d = md(x, y, sx, sy)
      if d <= r:
        dx = abs(x - sx)
        y = sy + (r - dx)
        break
    else:
      print(x, y)
      print(4000000*x+y)
      sys.exit()
        
    y += 1
  x += 1
