import sys

shapes = [[(0, 0), (0, 1), (0, 2), (0, 3)],
          [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
          [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
          [(0, 0), (1, 0), (2, 0), (3, 0)],
          [(0, 0), (0, 1), (1, 0), (1, 1)]]
shifts = sys.stdin.read().strip()
n_shifts = len(shifts)
print(n_shifts)

height = 0
i = 0
shiftPos = 0
grid = [
  [0] * 7,
  [0] * 7,
  [0] * 7,
  [0] * 7,
  [0] * 7,
  [0] * 7,
  [0] * 7,
]

def blocked(shape, x, y):
  for off_y, off_x in shape:
    if x < 0 or y < 0 or (x + off_x > 6) or grid[y + off_y][x + off_x]:
      return True
  return False

def printGrid():
  for line in grid[::-1]:
    print('|' + ''.join(['#' if s else ' ' for s in line]) + '|')
  print('+-------+')

been = set()
heights = []
while i < 2755:
  #printGrid()
  x, y = 2, height + 3
  shape = shapes[i%5]
  if (i%5, shiftPos) in been:
    print(i, i%5, shiftPos, height)
  else:
    been.add((i%5, shiftPos))
  i += 1
  while True:
    shift = shifts[shiftPos]
    shiftPos = (shiftPos+1)%n_shifts
    if shift == '<' and not blocked(shape, x - 1, y):
      x -= 1
    elif shift == '>' and not blocked(shape, x + 1, y):
      x += 1

    if not blocked(shape, x, y - 1):
      y -= 1
    else:
      height = max(height, y + shape[-1][0] + 1)
      while len(grid) < height + 7:
        grid.append([0] * 7)
      for off_y, off_x in shape:
        grid[y + off_y][x + off_x] = 1
      break

print(height)
