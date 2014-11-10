from pyhop import *

import hanoi_methods

state = State('hanoi-state')
state.disk = list(range(1, 12))
state.pole = {'p1': list(reversed(range(1, 12))), 'p2': [], 'p3': []}

pyhop(state, [("move_stack", 0, 'p1', 'p3', 'p2')], verbose=1)
