import sys
import functools

answer = 0
rows = []
for line in sys.stdin.readlines():
  line = line.rstrip()
  rows.append([int(x) for x in line])

cols = [[] for i in range(len(rows[0]))]
for i, row in enumerate(rows):
  for j, cell in enumerate(row):
    cols[j].append(cell)
    
  
visible = 0
height = len(rows)
width = len(cols)
for i, row in enumerate(rows):
  for j, cell in enumerate(row):
    if not i or cell > max(cols[j][0:i]):
      answer += 1
      continue
    if not j or cell > max(rows[i][0:j]):
      answer += 1
      continue
    if ((i+1) == height) or cell > max(cols[j][i+1:]):
      answer += 1
      continue
    if ((j+1) == width) or cell > max(rows[i][j+1:]):
      answer += 1
      continue

print(answer)

answer = 0
for i, row in enumerate(rows):
  for j, cell in enumerate(row):
    my_row = cols[j]
    my_col = rows[i]
    ss = [0]
    if j != width:
      for t in my_col[j+1:]:
        ss[-1] += 1
        if t >= cell:
          break
    ss.append(0)
    if i != height:
      for t in my_row[i+1:]:
        ss[-1] += 1
        if t >= cell:
          break
    ss.append(0)
    if j:
      for t in my_col[j-1::-1]:
        ss[-1] += 1
        if t >= cell:
          break
    ss.append(0)
    if i:
      for t in my_row[i-1::-1]:
        ss[-1] += 1
        if t >= cell:
          break
    answer = max(answer, functools.reduce(lambda x, y: x*y, ss, 1))



print(answer)
