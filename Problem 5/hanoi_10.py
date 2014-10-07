from pyhop import *
import hanoi_domain

state = State('hanoi-state')
state.diskLocation = [1 for i in range(0, 10)]

pyhop(state, [('move', 10, 1, 3)], verbose=1)
