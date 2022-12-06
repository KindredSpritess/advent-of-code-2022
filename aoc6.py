import sys

for line in sys.stdin.readlines():
  line = line.rstrip()
  cur = set()
  for i in range(len(line)):
    if i >= 14:
      if len(set(line[i-14:i])) == 14:
        print(i)
        sys.exit(0)
