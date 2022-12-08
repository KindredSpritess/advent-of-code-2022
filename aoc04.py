import sys


t = 0
for line in sys.stdin.readlines():
  rs = line.strip().split(',')
  r1, r2 = (set(range(int(r.split('-')[0]), int(r.split('-')[1])+1)) for r in rs)
  if r1 & r2:
    t += 1

print(t)
  
