import collections
import sys

answer = None
elf_field = {}
elves = []

class Elf(object):
  def __init__(self, pos):
    self.pos = pos
    elf_field[pos] = self

  def predict(self, proposals, offsets):
    self.proposals = []
    for off in SURROUNDS:
      if self.pos + off in elf_field:
        break
    else:
      return
    for (off1, off2, off3, direction) in offsets:
      if self.pos + off1 in elf_field:
        continue
      if self.pos + off2 in elf_field:
        continue
      if self.pos + off3 in elf_field:
        continue

      self.proposals.append(self.pos + off2)
      proposals[self.pos + off2] += 1
      break

  def move(self, proposals):
    assert len(self.proposals) <= 1
    for p in self.proposals:
      if proposals[p] == 1:
        del elf_field[self.pos]
        elf_field[p] = self
        self.pos = p
        return True

    return False
    

for y, line in enumerate(sys.stdin.readlines()):
  line = line.rstrip()
  for x, c in enumerate(line):
    if c == '#':
      elves.append(Elf(complex(x,y)))

SURROUNDS = [
  -1-1j,
  -1j,
  1-1j,
  1,
  1+1j,
  -1,
  -1+1j,
  1j,
]
offsets = [
  (-1-1j, -1j, 1-1j, 'N'),
  (-1+1j,  1j, 1+1j, 'S'),
  (-1-1j, -1, -1+1j, 'W'),
  ( 1-1j,  1,  1+1j, 'E'),
]
i = 0
while True:
  i += 1
  proposals = collections.Counter()
  for elf in elves:
    elf.predict(proposals, offsets)
  incomplete = False
  for elf in elves:
    incomplete |= elf.move(proposals)

  if not incomplete:
    print(i)
    break

  offsets.append(offsets.pop(0))
  assert len(elves) == len(elf_field)
  assert len(offsets) == 4


minX, maxX, minY, maxY = 1e9, -1e9, 1e9, -1e9
for p in elf_field:
  minX = int(min(minX, p.real))
  maxX = int(max(maxX, p.real))
  minY = int(min(minY, p.imag))
  maxY = int(max(maxY, p.imag))

print(minX, maxX, minY, maxY)
print(((maxX - minX + 1) * (maxY - minY + 1)) - len(elves))
