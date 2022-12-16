import cProfile
import functools
import queue
import re
import sys
import collections

vertices = {}
start = None
target = None

class Node(object):

  def __init__(self, r, i):
    self.r = r
    self.id = i
    self.edges = []

  def add(self, v):
    self.edges.append(v)

  def value(self, t):
    return self.r * t

  def __str__(self):
    return (f'{chr(self.id)}: [{[chr(e.e) for e in self.edges]}]')

answer = None
lines = sys.stdin.readlines()
for line in lines:
  line = line.rstrip()
  name, rate, output = re.match(r'Valve (.*) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)', line).groups()
  vertices[name] = Node(int(rate), name)

for line in lines:
  line = line.rstrip()
  name, rate, output = re.match(r'Valve (.*) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)', line).groups()
  v = vertices[name]
  for out in output.split(', '):
    v.add(vertices[out])


def shortestPath(graph, source):
  dist = {}
  prev = {}
  q = queue.PriorityQueue()
  processed = set()
  for i, v in graph.items():
    dist[i] = 9999
    if v == source:
      dist[i] = 0
    prev[i] = None
    q.put((dist[i], i))

  while not q.empty():
    _, u = q.get()
    if u in processed:
      continue
    processed.add(u)
    for v in graph[u].edges:
      if v.id not in processed:
        alt = dist[u] + 1
        if alt < dist[v.id]:
          dist[v.id] = alt
          prev[v.id] = u
          q.put((alt, v.id))
    
  return dist, prev


distances = {}
paths = {}
for i, node in vertices.items():
  dist, prev = shortestPath(vertices, node)
  distances[i] = dist
  paths[i] = prev

print(' \t' + '\t'.join(sorted(vertices)))
for k in sorted(vertices):
  print(f'{k}\t' + '\t'.join([str(distances[k][i]) for i in vertices]))


off = tuple(sorted({v for v, n in vertices.items() if n.r}))

@functools.cache
def bestScore(at, t, off):
  s = vertices[at].value(t)
  if not off or t <= 0:
    return s

  ss = 0 
  nxtOff = tuple(n for n in off if n != at)
  for nxt in nxtOff:
    nxt_score = bestScore(nxt, t - 1 - distances[at][nxt], nxtOff)
    ss = max(ss, nxt_score)

  return s + ss

print(max(bestScore(x, 29 - distances['AA'][x], off) for x in off))
  
