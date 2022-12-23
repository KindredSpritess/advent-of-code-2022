import sys

class HumanError(Exception):
  pass

answer = None
terms = {}
exprs = {}
for line in sys.stdin.readlines():
  line = line.rstrip()
  term, expr = line.split(': ')
  if term == 'humn':
    expr = ' ifb  fasjfkfnbf '
  try:
    expr = int(expr)
    terms[term] = expr
  except ValueError:
    exprs[term] = expr
    
def evalTerm(name):
  if name == 'humn':
    raise HumanError
  if name in terms:
    return terms[name]
  a, op, b = exprs[name].split()
  if a not in terms:
    evalTerm(a)
  a = terms[a]
  if b not in terms:
    evalTerm(b)
  b = terms[b]
  if op == '+':
    terms[name] = a + b
  if op == '-':
    terms[name] = a - b
  if op == '/':
    terms[name] = a / b
  if op == '*':
    terms[name] = a * b
  return terms[name]


OPS = {
  'a+': '-',
  'b+': '-',
  'a-': '--',
  'b-': '+',
  'a*': '/',
  'b*': '/',
  'a/': 'inv',
  'b/': '*',
}


def evalHumn(n, expr):
  ops = []
  while expr != 'humn':
    a, op, b = exprs[expr].split()
    try:
      a = evalTerm(a)
      ops.append((OPS[f'a{op}'], a))
      expr = b
    except HumanError:
      b = evalTerm(b)
      ops.append((OPS[f'b{op}'], b))
      expr = a

  for op, term in ops:
    #print(op, term)
    if op == '-':
      n -= term
    elif op == '--':
      n -= term
      n *= -1
    elif op == '+':
      n += term
    elif op == '/':
      n /= term
    elif op == '*':
      n *= term
    elif op == 'inv':
      n = term / n
    else:
      raise HumanError(op)

  return n


def evalRoot():
  a, _, b = exprs['root'].split()
  try:
    a = evalTerm(a)
  except HumanError:
    return evalHumn(evalTerm(b), a)

  return evalHumn(a, b)
  

print(evalRoot())
