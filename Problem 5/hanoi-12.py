from pyhop import *
import hanoi_domain

state = State('hanoi-state')
state.diskLocation = [1 for i in range(0, 12)]

pyhop(state, [('move', 12, 1, 3)], verbose=1)
