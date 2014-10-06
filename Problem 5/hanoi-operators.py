import pyhop

def move_disk(state, disk, below, new_below, source, dest):
	if(state.on[disk] == below && 
	   state.top[source] == disk &&
	   state.top[dest] == new_below &&
	   state.size[disk] < state.size[below] &&
	   state.size[disk] < state.size[new_below] &&
	   below != new_below &&
	   disk != below &&
	   disk != new_below &&
	   source != dest)
		state.on[disk] = new_below
		state.top[source] = below
		state.top[dest] = disk
	else:
		print 'something goofed'

pyhop.declare_operators(move_disk)