import re
import sys

answer = None
lines = sys.stdin.readlines()
grid = []
maxWidth = 0
for line in lines[:-2]:
  line = line.rstrip()
  maxWidth = max(len(line), maxWidth)

for line in lines[:-2]:
  line = line.rstrip()
  grid.append(list(line))
  grid[-1].extend([' '] * (maxWidth - len(line)))

x, y = grid[0].index('.'), 0
d = 0

def nextSquare():
  xx, yy = x, y
  if d == 0:
    xx = (xx+1)%maxWidth
    while grid[yy][xx] == ' ':
      xx = (xx+1)%maxWidth
  elif d == 2:
    xx = (xx-1)%maxWidth
    while grid[yy][xx] == ' ':
      xx = (xx-1)%maxWidth
  elif d == 1:
    yy = (yy+1)%len(grid)
    while grid[yy][xx] == ' ':
      yy = (yy+1)%len(grid)
  elif d == 3:
    yy = (yy-1)%len(grid)
    while grid[yy][xx] == ' ':
      yy = (yy-1)%len(grid)

  return xx, yy


def move():
  global x, y
  x, y = nextSquare()


def unblocked():
  xx, yy = nextSquare()
  print(xx, yy, grid[yy][xx] != '#')
  return grid[yy][xx] != '#'
  

instructions = re.split(r'([0-9]*)([LR])', lines[-1])  
for ins in filter(None, instructions):
  print(x,y,d,ins)
  if ins == 'R':
    d = (d+1)%4
  elif ins == 'L':
    d = (d-1)%4
  else:
    steps = int(ins)
    while steps and unblocked():
      move()
      steps -= 1

print(x, y, d)
print(1000 * (y+1) + 4 * (x+1) + d)
