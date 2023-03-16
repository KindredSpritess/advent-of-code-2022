import sys

answer = 0
for line in sys.stdin.readlines():
  line = line.rstrip()
  nn = 0
  for c in line:
    nn *= 5
    if c == '-':
      n = -1
    elif c == '=':
      n = -2
    else:
      n = int(c)
    nn += n 
  answer += nn

def snafu(n):
  snafu = ''
  carry = 0
  while n:
    c = (n+carry) % 5
    if c >= 3:
      carry = 1
    else:
      carry = 0
    if c == 3:
      c = '='
    elif c == 4:
      c = '-'
    snafu = str(c) + snafu
    n //= 5
  if carry:
    snafu = str(carry) + snafu
  return snafu

print(snafu(answer))
