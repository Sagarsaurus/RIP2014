from pyhop import *
import hanoi_domain

state = State('hanoi-state')
for i in range(1,11):
	state.diskLocation[i] = 1

pyhop(state, [('move', 10, 1, 3)], verbose=1)
