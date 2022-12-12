import sys

vertices = []
start = None
target = None

class Node(object):

  def __init__(self, e, i):
    self.e = ord(e)
    self.id = i
    self.edges = []

  def add(self, v):
    self.edges.append(v)

  def __str__(self):
    return (f'{chr(self.e)}: [{[chr(e.e) for e in self.edges]}]')

answer = None
for line in sys.stdin.readlines():
  line = line.rstrip()
  for c in line:
    i = len(vertices)
    if c == 'S':
      start = Node('a', i)
      vertices.append(start)
    elif c == 'E':
      target = Node('z', i)
      vertices.append(target)
    else:
      vertices.append(Node(c, i))

    # Check left, and up.
    l = i - 1
    u = i - len(line)
    if u >= 0:
      # Check direction
      if vertices[i].e <= vertices[u].e or vertices[i].e - 1 == vertices[u].e:
        vertices[i].add(vertices[u])
      if vertices[i].e >= vertices[u].e or vertices[i].e == vertices[u].e - 1:
        vertices[u].add(vertices[i])
    if l // len(line) == i // len(line):
      # Check direction
      if vertices[i].e <= vertices[l].e or vertices[i].e - 1 == vertices[l].e:
        vertices[i].add(vertices[l])
      if vertices[i].e >= vertices[l].e or vertices[i].e == vertices[l].e - 1:
        vertices[l].add(vertices[i])

#for v in vertices:
#  print(v)
      
def shortestPath(graph, source):
  dist = {}
  prev = {}
  q = set()
  for i, v in enumerate(graph):
    dist[i] = 9999
    if v == source:
      dist[i] = 0
    prev[i] = None
    q.add(i)

  while q:
    u = sorted(q, key=lambda i: dist[i])[0]
    q.remove(u)
    for v in graph[u].edges:
      if v.id in q:
        alt = dist[u] + 1
        if alt < dist[v.id]:
          dist[v.id] = alt
          prev[v.id] = u
    
  return dist, prev
    
#dists, prevs = shortestPath(vertices, start)
#print(dists[target.id])

import cProfile
import pstats
import io
from pstats import SortKey

with cProfile.Profile() as pr:
  dists, prevs = shortestPath(vertices, target)
  print(sorted([(dists[v.id], v.id) for v in vertices if chr(v.e) == 'a'])[0])
pr.print_stats()

def bfs(graph, s):
  cur = set([s.id])
  visited = set()
  steps = 0

  while True:
    nxt = set()
    for i in cur:
      visited.add(i)
      if graph[i].e == 97:
        return steps
      for edge in graph[i].edges:
        if edge.id not in visited:
          nxt.add(edge.id)
    
    cur = nxt
    steps += 1
    
with cProfile.Profile() as pr:
  print(bfs(vertices, target))
pr.print_stats()

