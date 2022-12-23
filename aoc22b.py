import math
import re
import sys

answer = None
lines = sys.stdin.readlines()
faces = {}
faces_xy = {}

D = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}

class Face(object):
  def __init__(self, x, y, spot):
    self.spot = spot
    self.x = x
    self.y = y
    self.d = 0
    self.grid = []
    self.edges = {}

WIDTH = 50
for i, line in enumerate(lines[:-2]):
  line = line.rstrip()
  num_faces = len(line) // WIDTH
  sect = i // WIDTH
  for j in range(num_faces):
    face_line = line[j*WIDTH:(j+1)*WIDTH]
    if not face_line.strip():
      continue
    face = faces_xy.get((j, sect))
    if not face:
      face = Face(j*WIDTH, i, (j, sect))
      if (0, 0) not in faces:
        face.d = 0
        faces[(0, 0)] = face
      faces_xy[(j, sect)] = face
        
    face.grid.append(face_line)


def normalize(x, y):
  if abs(x) == 180:
    x = 0
    y -= 180
  if y == -180:
    y = 180
  if y == 270:
    y = -90
  if abs(x) == 90:
    y = 0
  return x, y


def rotate(lat, lng, br):
  br %= 4
  if lat == 0 and br == 1:
    lat, lng = -90, 0
  elif lat == 0 and br == 3:
    lat, lng = 90, 0
  elif lat == 0:
    lat, lng = 0, (lng + 90 * (br+1)) % 360
  elif lat == 90:
    lat, lng, br = 0, (br-1)*90%360, 1
  else:
    lat, lng, br = 0, (br+1)*90%360, 3
  
  return normalize(lat, lng), br


def nxt(direction, x, y):
  direction %= 4
  if direction == 0:
    return x+1, y
  elif direction == 1:
    return x, y+1
  elif direction == 2:
    return x-1, y
  elif direction == 3:
    return x, y-1


def fillFaces(lat, lng, facing, bearing):
    global faces
    node = faces[(lat, lng)]
    i, j = node.spot
    f = nxt(facing, i, j)
    l = nxt(facing - 1, i, j)
    r = nxt(facing + 1, i, j)
    if f in faces_xy:
      (lat1, lng1), br = rotate(lat, lng, bearing)
      faces[(lat1, lng1)] = faces_xy[f]
      fillFaces(lat1, lng1, facing, br)
    if l in faces_xy:
      (lat1, lng1), br = rotate(lat, lng, bearing-1)
      faces[(lat1, lng1)] = faces_xy[l]
      fillFaces(lat1, lng1, facing - 1, br)
    if r in faces_xy:
      (lat1, lng1), br = rotate(lat, lng, bearing+1)
      faces[(lat1, lng1)] = faces_xy[r]
      fillFaces(lat1, lng1, facing + 1, br)


fillFaces(0, 0, 1, 1)

for k, face in faces.items():
  print(k, face.spot)

for (x, y), face in faces_xy.items():
  if (x+1, y) in faces_xy:
    faces_xy[(x,y)].edges[0] = faces_xy[(x+1,y)]
  if (x, y+1) in faces_xy:
    faces_xy[(x,y)].edges[1] = faces_xy[(x,y+1)]
  if (x-1, y) in faces_xy:
    faces_xy[(x,y)].edges[2] = faces_xy[(x-1,y)]
  if (x, y-1) in faces_xy:
    faces_xy[(x,y)].edges[3] = faces_xy[(x,y-1)]


for face in faces.values():
  assert len(face.grid) == WIDTH
  for row in face.grid:
    assert len(row) == WIDTH

spots = set(range(WIDTH))

f, x, y = (0, 0), faces[(0, 0)].grid[0].index('.'), 0
d = 0
bearing = 0


WM1 = WIDTH - 1
ROUTES = {
  ((0,0),(90,0)):      lambda x, y: (0, x, 0),
  ((90,0),(0,0)):      lambda x, y: (y, 0, 1),
  ((0,0),(0,-90)):     lambda x, y: (0, WM1 - y, 0),
  ((0,-90),(0,0)):     lambda x, y: (0, WM1 - y, 0), 
  ((-90,0),(0,-90)):   lambda x, y: (y, 0, 1),
  ((0,-90),(-90,0)):   lambda x, y: (0, x, 0),
  ((-90,0),(0,90)):    lambda x, y: (y, WM1, 3),
  ((0,90),(-90,0)):    lambda x, y: (WM1, x, 2),
  ((0,180),(90,0)):    lambda x, y: (WM1, x, 2),
  ((90,0),(0,180)):    lambda x, y: (y, WM1, 3),
  ((0,180),(0,90)):    lambda x, y: (WM1, WM1 - y, 2),
  ((0,90),(0,180)):    lambda x, y: (WM1, WM1 - y, 2),
  ((90,0),(0,90)):     lambda x, y: (x, 0, 1),
  ((0,90),(90,0)):     lambda x, y: (x, WM1, 3),
}
assert len(ROUTES) == 14

PB = {0: 3, 90: 2, 180: 1, -90: 0}
BL = {3: 180, 2: -90, 1: 0, 0: 90}
SBL = {3: 180, 2: 90, 1: 0, 0: -90}


def rotate2(lat, lng, br):
  br %= 4
  if lat == 0 and br == 1:
    br = PB[lng]
    lat, lng = -90, 0
  elif lat == 0 and br == 3:
    br = PB[lng]
    lat, lng = 90, 0
  elif lat == 0:
    lat, lng = 0, (lng + 90 * (br+1)) % 360
  elif lat == 90:
    lat, lng, br = 0, BL[br], 1
  else:
    lat, lng, br = 0, BL[br], 3
  
  return normalize(lat, lng), br


def nextSquare():
  ff, xx, yy, dd, br = f, x, y, d, bearing
  if d == 0:
    xx += 1
  elif d == 2:
    xx -= 1
  elif d == 1:
    yy += 1
  elif d == 3:
    yy -= 1

  if xx not in spots or yy not in spots:
    lat, lng = ff
    ff, br = rotate2(lat, lng, br)
    print(D[d], 'new face', f, '->', ff)
  else:
    return ff, xx, yy, dd, br

  oldFace, newFace = faces[f], faces[ff]

  # If old face touches new face direction need not change.
  dx, dy = oldFace.spot[0] - newFace.spot[0], oldFace.spot[1] - newFace.spot[1]
  if abs(dx) + abs(dy) < 2:
    print('touching')
    return ff, xx % WIDTH, yy % WIDTH, dd, br

  xx, yy, dd = ROUTES[(f, ff)](xx, yy)

  return ff, xx, yy, dd, br


def move():
  global f, x, y, d, bearing
  f, x, y, d, bearing = nextSquare()


def unblocked():
  ff, xx, yy, _, _ = nextSquare()
  return faces[ff].grid[yy][xx] != '#'
  

instructions = re.split(r'([0-9]*)([LR])', lines[-1])  
for ins in filter(None, instructions):
  if ins == 'R':
    d = (d+1)%4
    bearing += -1 if f[0] == -90 else 1
    bearing %= 4
  elif ins == 'L':
    d = (d-1)%4
    bearing += 1 if f[0] == -90 else -1
    bearing %= 4
  else:
    steps = int(ins)
    while steps and unblocked():
      move()
      steps -= 1

print(f,x,y,d,bearing)
spot = faces[f].spot
x = spot[0]*WIDTH + x
y = spot[1]*WIDTH + y
print(1000 * (y+1) + 4 * (x+1) + d)
