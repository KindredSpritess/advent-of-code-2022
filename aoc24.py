import cProfile
import queue
import sys

answer = None

class Blizzard(object):

  def __init__(self, pos, direction):
    self.pos = pos
    self.direction = direction

  def move(self, occupied):
    self.pos += self.direction
    if self.pos.real < 0:
      self.pos = complex(WIDTH, self.pos.imag)
    elif self.pos.real > WIDTH:
      self.pos = complex(0, self.pos.imag)
    elif self.pos.imag == 0:
      self.pos = complex(self.pos.real, HEIGHT-1)
    elif self.pos.imag >= HEIGHT:
      self.pos = complex(self.pos.real, 1)
    occupied.add(self.pos)

blizzards = []
lines = sys.stdin.readlines()
WIDTH = len(lines[1].strip()) - 3
HEIGHT = len(lines) - 1
for j, line in enumerate(lines):
  line = line.rstrip()
  for i, c in enumerate(line[1:-1]):
    if c == '>':
      blizzards.append(Blizzard(complex(i, j), 1))
    elif c == '<':
      blizzards.append(Blizzard(complex(i, j), -1))
    elif c == 'v':
      assert i not in (0, WIDTH)
      blizzards.append(Blizzard(complex(i, j), 1j))
    elif c == '^':
      assert i not in (0, WIDTH)
      blizzards.append(Blizzard(complex(i, j), -1j))


pos = origin = complex(lines[0].index('.')-1,0)
destination = complex(lines[-1].index('.')-1,len(lines)-1)
print(origin, destination)


def inBounds(position):
  if position in (origin, destination):
    return True
  if position.real < 0 or position.real > WIDTH:
    return False
  return position.imag > 0 and position.imag < HEIGHT


legalMoves = [
  1, -1, 1j, -1j, 0
]
pat = set()
q = queue.SimpleQueue()
entry = (0, pos, 0)
q.put(entry)
pat.add(entry)
CLOCK = 0
occupied = set()
try:
  with cProfile.Profile() as pr:
    while True:
      t, pos, target = q.get()
      t += 1
      while CLOCK < t:
        occupied = set()
        for b in blizzards:
          b.move(occupied)
        CLOCK += 1
        #print(t, occupied)
      
      for m in legalMoves:
        nxt = m + pos
        if target % 2 and nxt == origin:
          target = 2
        elif not target % 2 and nxt == destination:
          if target:
            print(t)
            sys.exit()
          target = 1
        entry = t, nxt, target
        if inBounds(nxt) and nxt not in occupied and entry not in pat:
          pat.add(entry)
          q.put(entry)
finally:
  pr.print_stats()
