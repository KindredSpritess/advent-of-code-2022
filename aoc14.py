import sys


max_x = max_y = 0

lines = [l.strip() for l in sys.stdin.readlines()]
for line in lines:
  rocks = [[int(r) for r in rock.split(',')] for rock in line.split(' -> ')]
  for x, y in rocks:
    max_x = max(x, max_x)
    max_y = max(y, max_y)

grid = []
for y in range(max_y + 3):
  row = []
  for x in range(max_x + 500):
    if y == max_y + 2:
      row.append('#')
    else:
      row.append('.')
  grid.append(row)

for line in lines:
  line = line.rstrip()
  rocks = [[int(r) for r in rock.split(',')] for rock in line.split(' -> ')]
  for i, (x, y) in enumerate(rocks):
    if not i:
      continue
    ox, oy = rocks[i-1]
    if ox == x:
      y1, y2 = sorted([oy, y])
      for ry in range(y1, y2 + 1):
        grid[ry][x] = '#'
    elif oy == y:
      x1, x2 = sorted([ox, x])
      for rx in range(x1, x2 + 1):
        grid[y][rx] = '#'


answer = 0
while True:
  sx, sy = 500, 0
  while True:
    #if sy > max_y:
    #  print(answer)
    #  sys.exit()

    if grid[sy + 1][sx] == '.':
      sy += 1
    elif grid[sy + 1][sx - 1] == '.':
      sy += 1
      sx -= 1
    elif grid[sy + 1][sx + 1] == '.':
      sy += 1
      sx += 1
    else:
      grid[sy][sx] = 'o'
      answer += 1
      if sy == 0 and sx == 500:
        print(answer)
        sys.exit()
      break

