import sys

monkeys = []

class Item(object):
  def __init__(self, v):
    self.v = v

  def init(self, tvs):
    self.tvs = tvs
    self.vs = [self.v % tv for tv in tvs]

  def __add__(self, x):
    for i, tv in enumerate(self.tvs):
      self.vs[i] = (self.vs[i] + x) % tv
    return self

  def __mul__(self, x):
    if isinstance(x, Item):
      for i, tv in enumerate(self.tvs):
        self.vs[i] = (self.vs[i] * x.vs[i]) % tv
    else:
      for i, tv in enumerate(self.tvs):
        self.vs[i] = (self.vs[i] * x) % tv
    return self

  def __repr__(self):
    return str(self.vs)

class Monkey(object):
  def __init__(self):
    self.items = []
    self.operation = None
    self.tv = None
    self.t1 = None
    self.t2 = None
    self.count = 0

  def round(self):
    for item in self.items:
      self.count += 1
      item = self.operation(item)
      #item //= 3
      if item.vs[self.tv]:
        monkeys[self.t2].items.append(item)
      else:
        monkeys[self.t1].items.append(item)
    self.items = []

  def __str__(self):
    return str(self.items)

mul = lambda x: lambda old: old * x
add = lambda x: lambda old: old + x
tvs = []

for line in sys.stdin.readlines():
  line = line.strip()
  if line.startswith('Monkey'):
    monkeys.append(Monkey())
  elif line.startswith('Starting items:'):
    monkeys[-1].items = [Item(int(i)) for i in (line.split(': ')[1]).split(',')]
  elif line.startswith('Operation:'):
    op = line.split(' = ')[-1]
    if op == 'old * old':
      monkeys[-1].operation = lambda old: old * old
    else:
      _, o, b = op.split()
      b = int(b)
      if o == '+':
        monkeys[-1].operation = add(b)
      elif o == '*':
        monkeys[-1].operation = mul(b)
  elif line.startswith('Test:'):
    monkeys[-1].tv = len(tvs)
    tvs.append(int(line.split()[-1]))
  elif line.startswith('If true:'):
    monkeys[-1].t1 = int(line.split()[-1])
  elif line.startswith('If false:'):
    monkeys[-1].t2 = int(line.split()[-1])

for monkey in monkeys:
  for item in monkey.items:
    item.init(tvs)

for r in range(10000):
  for monkey in monkeys:
    monkey.round()

answer = sorted(monkeys, key=lambda x: x.count, reverse=True)

print(answer[0].count, answer[1].count)
