import sys
import re
import os
from collections import defaultdict

cwd = '/'
sizes = defaultdict(int)
total = 0

for line in sys.stdin.readlines():
  line = line.strip()
  if line[0] == '$':
    cmd = line.split()
    if cmd[1] == 'cd':
      cwd = os.path.abspath(os.path.join(cwd, cmd[2]))
  else:
    size, name = line.split()
    if size == 'dir':
      continue
    pwd = cwd
    size = int(size)
    total += size
    while pwd != '/':
      sizes[pwd] += size
      pwd = os.path.dirname(pwd)

output = 0
for size in sizes.values():
  if size <= 100000:
    output += size

print(output)
print('')

required = 30000000 - (70000000 - total)
print(required)

minSuitable = 30000000
for size in sizes.values():
  if size > required and size < minSuitable:
    minSuitable = size

print(minSuitable)

