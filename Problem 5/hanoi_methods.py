import pyhop

def move_stack(state, disk, src, dst, spare):
  print(disk, src, dst, spare)
  print(state.pole['p1'], state.pole['p2'], state.pole['p3'])
  if len(state.pole[src]) == disk:
    state.pole[dst].append(state.pole[src].pop())
    return []
  else:
    return [  ("move_stack", disk + 1, src, spare, dst),
              ("move_stack", disk, src, dst, spare),
              ("move_stack", len(state.pole[spare]), spare, dst, src) ]

pyhop.declare_methods('move_stack', move_stack)
