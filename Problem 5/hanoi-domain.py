import pyhop

def move_disk(state, disk, below, new_below, source, dest):
	if(state.disk[disk] == True &&
	   state.on[disk] == below &&
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

def hanoi_sub(state, disk_size, source, dest, via):
	disk = [item for item, size in state.size.items() if size == disk_size][0]
	below = [below for top, below in state.on.items() if top = disk][0]
	new_below = state.top[dest]
	if(disk_size == 1):
		return [('move_disk', disk, below, new_below, source, dest)]
	else:
		return [('hanoi_sub', disk_size - 1, source, via, dest), 
				('move_disk', disk, below, new_below, source, dest),
				('hanoi_sub', disk_size - 1, via, dest, source)]
				
pyhop.declare_methods('hanoi-sub', hanoi_sub)
