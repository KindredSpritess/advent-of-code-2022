import queue
import sys
import collections

answer = None
faces = set()
faceCount = collections.defaultdict(int)
drops = set()
dim = 0

def add(c):
  faces.add(c)
  faceCount[c] += 1

def surrounds(cube):
  x, y, z = cube
  yield (x+1, y, z)
  yield (x-1, y, z)
  yield (x, y+1, z)
  yield (x, y-1, z)
  yield (x, y, z+1)
  yield (x, y, z-1)

for line in sys.stdin.readlines():
  x, y, z = map(int, line.rstrip().split(','))
  dim = max(dim, x, y, z)
  drops.add((x,y,z))
  for s in surrounds((x,y,z)):
    add(s)

openCubes = faces - drops
openFaces = sum(faceCount[c] for c in openCubes)
print(openFaces)

visited = set()
q = queue.Queue()
q.put((-1, -1, -1))
res = 0
while not q.empty():
  c = q.get()
  visited.add(c)
  
  for n in surrounds(c):
    if min(n) < -2 or max(n) > dim + 2:
      continue
    if n in visited:
      continue
    if n in drops:
      res += 1
    else:
      visited.add(n)
      q.put(n)

print(res)
