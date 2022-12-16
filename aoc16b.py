import cProfile
import functools
import itertools
import queue
import re
import sys
import collections

vertices = {}
start = None
target = None

class Node(object):
  """Simple node in a graph with a flow rate r."""

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

# Construct all the nodes.
for line in lines:
  line = line.rstrip()
  name, rate, output = re.match(r'Valve (.*) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)', line).groups()
  vertices[name] = Node(int(rate), name)

# Connect to all neighbours.
for line in lines:
  line = line.rstrip()
  name, rate, output = re.match(r'Valve (.*) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)', line).groups()
  v = vertices[name]
  for out in output.split(', '):
    v.add(vertices[out])


# Dykstra, create minimum spanning tree.
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


# For each node, work out the spanning tree and save the distances.
distances = {}
for i, node in vertices.items():
  dist, prev = shortestPath(vertices, node)
  distances[i] = dist

# We really only need the nodes with flow rates everything else was just a distance.
off = tuple(sorted({v for v, n in vertices.items() if n.r}))

@functools.cache
def bestScore(at1, at2, t1, t2, off):
  """Recursive, calculate best possible score for remaining nodes.

  For the sake of memoization require t1 >= t2, they're equivalent anyway.
  """
  assert t1 >= t2
  if t1 > t2:
    s = vertices[at1].value(t1)

    nxtOff = tuple(n for n in off if n != at1 and n != at2)
    if not nxtOff:
      return s + vertices[at2].value(t2)

    if t1 <= 0:
      return 0

    ss = 0 
    for nxt in nxtOff:
      nt1 = max(0, t1 - 1 - distances[at1][nxt])
      if nt1 >= t2:
        nxt_score = bestScore(nxt, at2, nt1, t2, nxtOff)
      else:
        nxt_score = bestScore(at2, nxt, t2, nt1, nxtOff)
      ss = max(ss, nxt_score)

    return s + ss

  else:
    s_me = vertices[at1].value(t1)
    s_el = vertices[at2].value(t2)

    nxtOff = tuple(n for n in off if n != at1 and n != at2)
    if not nxtOff:
      return s_me + s_el

    if t1 <= 0:
      return 0

    ss = 0
    for nxt in nxtOff:
      nxt_score_me = bestScore(at2, nxt, t2, max(0, t1 - 1 - distances[at1][nxt]), nxtOff)
      nxt_score_el = bestScore(at1, nxt, t1, max(0, t2 - 1 - distances[at2][nxt]), nxtOff)
      ss = max(ss, nxt_score_me + s_me, nxt_score_el + s_el)

    return ss

  
# Obviously the elephant and me are equivalent, but our choices of starting destinations
# could any pair. Figure out which starting pair gives the best score.
starting = itertools.combinations(off, 2)
answer = 0
for me, el in starting:
  me_t = 25 - distances['AA'][me]
  el_t = 25 - distances['AA'][el]
  if me_t < el_t:
    answer = max(answer, bestScore(el, me, el_t, me_t, off))
  else:
    answer = max(answer, bestScore(me, el, me_t, el_t, off))
print(answer)
