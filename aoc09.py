import sys

cmds = [line.rstrip().split() for line in sys.stdin.readlines()]

# This was probably a mistake. It was probably better to just use pairs.
width = height = 0
maxWidth = maxHeight = 0
minHeight = minWidth = 0
for dir, val  in cmds:
  val = int(val)
  if dir == 'U':
    height += val
  elif dir == 'D':
    height -= val
  elif dir == 'R':
    width += val
  elif dir == 'L':
    width -= val
  maxWidth = max(width, maxWidth)
  maxHeight = max(height, maxHeight)
  minWidth = min(width, minWidth)
  minHeight = min(height, minHeight)

dim = max(maxHeight-minHeight+1, maxWidth-minWidth+1)

def touch(h, t):
  hx, hy = h // dim, h % dim
  tx, ty = t // dim, t % dim

  diffx = abs(hx - tx)
  diffy = abs(hy - ty)

  if max(diffx, diffy) > 1:
    if hx == tx:
      if hy < ty:
        t -= 1
      else:
        t += 1
    elif hy == ty:
      if hx < tx:
        t -= dim
      else:
        t += dim
    else:
      if hx < tx:
        t -= dim
      if hx > tx:
        t += dim
      if hy < ty:
        t -= 1
      if hy > ty:
        t += 1 

  return t


s = -minWidth - (minHeight * dim)
k = [s for _ in range(10)]
been = set([s])
for dir, val in cmds:
  val = int(val)
  for i in range(val):
    # Move head
    if dir == 'R':
      k[0] += 1
    if dir == 'L':
      k[0] -= 1
    if dir == 'U':
      k[0] += dim
    if dir == 'D':
      k[0] -= dim

    # Check if tail needs to move
    for i in range(9):
      k[i+1] = touch(k[i], k[i+1])
      
    been.add(k[9])
  

print(len(been))
