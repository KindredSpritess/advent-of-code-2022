import sys

# There's probably a bounds issue here at the last char.
N=14
# sys.stdin.read() would have worked for this problem, just in a habit.
for line in sys.stdin.readlines():
  line = line.rstrip()
  for i in range(len(line)):
    if i >= N:
      if len(set(line[i-N:i])) == N:
        print(i)
        sys.exit(0)
