import collections
import math
import re
import sys

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

class Counter(collections.Counter):

  def __mul__(self, other):
    assert isinstance(other, int)
    res = Counter()
    for key in self:
      res[key] = self[key] * other
    return res

  def __add__(self, other):
    return Counter(super().__add__(other))
    

def MostGeodes(costs, t):
  robots = Counter({ORE:1})
  available = Counter()

  q = collections.deque()
  q.append((t, available, robots))
  highestGeodes = 0
  print(costs)

  while q:
    t, available, robots = q.popleft()
    #print(t, robots, available)
    geodes = available[GEODE] + t*robots[GEODE]
    if geodes + (t**2+t)/2 < highestGeodes:
      continue
    if geodes > highestGeodes:
      highestGeodes = geodes
      #print(geodes)
    t -= 1

    # Calculate max per robot.
    worth_constructing = {GEODE}
    for robot in costs:
      for res, cost in robot.items():
        if robots[res] >= cost:
          continue
        #if robots[res]*(t+1)+available[res] >= (t*cost):
        #  continue

        worth_constructing.add(res)

    for robot in worth_constructing:
      cost = costs[robot]
      minutes = 0
      for res, amt in cost.items():
        if res not in robots:
          break
        minutes = max(minutes, (amt - available[res]) / robots[res])
      else:
        minutes = int(math.ceil(minutes))
        #print(t, robot, minutes)
        if minutes < t:
          q.appendleft((t-minutes, available + (robots*(minutes+1)) - cost, robots + Counter({robot:1})))
        
  print(highestGeodes)
  return highestGeodes
    
  

answer = 1
for line in sys.stdin.readlines():
  line = line.rstrip()
  groups = list(map(int, re.match(r'Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.', line).groups()))
  bp = groups[0]
  costs = (
      Counter({ORE: groups[1]}),
      Counter({ORE: groups[2]}),
      Counter({ORE: groups[3], CLAY: groups[4]}),
      Counter({ORE: groups[5], OBSIDIAN: groups[6]})
  )
  #answer += bp * MostGeodes(costs, 24)
  answer *= MostGeodes(costs, 32)
  if bp == 3:
    break
  
print(answer)
