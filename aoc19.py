from collections import Counter
import queue
import re
import sys

def MostGeodes(costs):
  t = 24
  robots = Counter(ore=1)
  available = Counter()

  q = queue.PriorityQueue()
  q.put((t, available, robots))
  highestGeodes = 0
  print(costs)
  maxCost = costs[0] | costs[1] | costs[2] | costs[3]

  while not q.empty():
    t, available, robots = q.get()
    if t == 0:
      highestGeodes = max(highestGeodes, available['geode'])
      #print(highestGeodes)
      continue
    t -= 1
    if costs[3] <= available:
      q.put((t, available - costs[3] + robots, robots + Counter(geode=1)))

    # If no way of getting enough, stop.
    rpm = 1
    for res, amt in costs[3].items():
      if not robots[res]:
        rpm = 0
        break
      rpm = min(rpm, amt / robots[res])
      
    maxGeodeBreakers = robots['geode'] + (t-1) * rpm
    if t < 4 and (maxGeodeBreakers + maxGeodeBreakers**2) / 2 + available['geode'] <= highestGeodes:
      #print('pruned', t, robots, q.qsize())
      continue

    queueable = []
    if costs[2] <= available and robots['obsidian'] < maxCost['obsidian']:
      queueable.append((t, available - costs[2] + robots, robots + Counter(obsidian=1)))
    if costs[1] <= available and robots['clay'] < maxCost['clay']:
      queueable.append((t, available - costs[1] + robots, robots + Counter(clay=1)))
    if costs[0] <= available and robots['ore'] < maxCost['ore']:
      queueable.append((t, available - costs[0] + robots, robots + Counter(ore=1)))
    queueable.append((t, available + robots, robots))
    for e in queueable[:2]:
      q.put(e)

  print(highestGeodes)
  return highestGeodes
    
  

answer = 0
for line in sys.stdin.readlines():
  line = line.rstrip()
  groups = list(map(int, re.match(r'Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.', line).groups()))
  bp = groups[0]
  costs = (
      Counter(ore=groups[1]),
      Counter(ore=groups[2]),
      Counter(ore=groups[3], clay=groups[4]),
      Counter(ore=groups[5], obsidian=groups[6])
  )
  answer += bp * MostGeodes(costs)
  
print(answer)
