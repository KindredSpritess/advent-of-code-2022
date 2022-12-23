import sys

answer = None
terms = {}
exprs = {}
for line in sys.stdin.readlines():
  line = line.rstrip()
  term, expr = line.split(': ')
  try:
    expr = int(expr)
    terms[term] = expr
  except ValueError:
    exprs[term] = expr
    
def evalTerm(name):
  if name in terms:
    return name
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
  

print(evalTerm('root'))
