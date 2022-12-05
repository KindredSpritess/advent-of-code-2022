from collections import defaultdict
import re
import sys

lines = [l.rstrip() for l in sys.stdin.readlines()]

stacks = defaultdict(list)
stackIds = {}

for line in lines:
  if line.startswith('move'):
    q, s, d = re.match(r'^move (\d+) from (\d+) to (\d+)$', line).groups()
    q = int(q)
    stacks[stackIds[d]].extend(stacks[stackIds[s]][-q:])
    for _ in range(q):
      stacks[stackIds[s]].pop()
    #for _ in range(int(q)):
      #stacks[stackIds[d]].append(stacks[stackIds[s]].pop())
  else:
    i = 0
    while (i*4) < len(line):
      if line[i*4] == '[':
        stacks[i].insert(0, line[i*4+1])
      elif line[i*4+1] != ' ':
        stackIds[line[i*4+1]] = i
      i += 1

for i in range(len(stacks)):
  print(stacks[i][-1], end="")
print()
