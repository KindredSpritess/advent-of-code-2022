import sys

answer = []
ins = []
for line in sys.stdin.readlines():
  line = line.rstrip()
  ins.append(0)
  if line.startswith('addx'):
    v = int(line.split()[-1])
    ins.append(v)

screen = []
X = 1
for i, v in enumerate(ins):
  if i % 40 == 19:
   answer.append((i+1) * X)
  if i % 40 == 0:
    screen.append([])
  if abs(X - (i % 40)) < 2:
    screen[-1].append('#')
  else:
    screen[-1].append(' ')

  X += v 
    

print(sum(answer))
print('\n'.join([''.join(l) for l in screen]))
