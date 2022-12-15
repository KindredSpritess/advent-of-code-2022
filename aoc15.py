import re
import sys

answer = set()
beacons = set()
q = 2000000
for line in sys.stdin.readlines():
  line = line.rstrip()
  sx, sy, bx, by = map(int, re.match(r'Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)', line).groups())
  if by == q:
    beacons.add(bx)
  d = abs(sx - bx) + abs(sy - by)
  dr = d - abs(sy - q) + 1
  if dr <= 0:
    continue
  for i in range(sx - dr + 1, sx + dr):
    answer.add(i)
    
print(len(answer - beacons))
