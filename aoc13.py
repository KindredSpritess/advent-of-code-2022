from itertools import zip_longest
import sys

class Packet(list):

  def __lt__(self, other):
    for x, y in zip_longest(self, other, fillvalue=-100000000000000):
      if isinstance(x, int) and isinstance(y, int):
        if x != y:
          return x < y
        continue
      elif isinstance(x, int):
        x = [x]
      elif isinstance(y, int):
        y = [y]

      if Packet.__lt__(x, y):
        return True
      if Packet.__lt__(y, x):
        return False

    return False


answer = 0
lines = iter(sys.stdin.read().replace('\n\n', '\n').split('\n'))
packets = [Packet([[2]]), Packet([[6]])]
for i, (p1, p2) in enumerate(zip(lines, lines)):
  packets.append(Packet(eval(p1)))
  packets.append(Packet(eval(p2)))
  if packets[-2] < packets[-1]:
    answer += i + 1

print(answer)
packets.sort()
print((packets.index([[2]]) + 1) * (packets.index([[6]]) + 1))
