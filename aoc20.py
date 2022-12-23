import sys

KEY = 811589153
class N(object):
  
  def __init__(self, i, id):
    self.i = i * KEY
    self.id = id

  def __eq__(self, id):
    return id == self.id

  def __str__(self):
    return str(self.i)


zid = None
items = []
for line in sys.stdin.readlines():
  if not int(line):
    zid = len(items)
  items.append(N(int(line.strip()), len(items)))

moves = items[:]

MIXES = 10
for _ in range(MIXES):
  for move in moves:
    if not move.i:
      continue
    pos = items.index(move.id)
    item = items.pop(pos)
    if move.i > 0:
      pos = (pos + move.i) % len(items)
    else:
      pos = (pos + move.i) % len(items)
    items.insert(pos, item)

offset = items.index(zid)
a1 = (items[(offset+1000)%len(items)].i)
a2 = (items[(offset+2000)%len(items)].i)
a3 = (items[(offset+3000)%len(items)].i)
print(a1+a2+a3, a1, a2, a3)
