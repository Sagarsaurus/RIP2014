import pyhop

def move_disk(state, disk, below, new_below, source, dest):
	if(state.disk[disk] == True and 
	   state.on[disk] == below and
	   state.top[source] == disk and
	   state.top[dest] == new_below and
	   state.size[disk] < state.size[below] and
	   state.size[disk] < state.size[new_below] and
	   below != new_below and
	   disk != below and
	   disk != new_below and
	   source != dest):
		state.on[disk] = new_below
		state.top[source] = below
		state.top[dest] = disk
	else:
		print 'something goofed'

pyhop.declare_operators(move_disk)

def hanoi_sub(state, disk_size, source, dest, via):
	disk = [item for item, size in state.size.items() if size == disk_size][0]
	below = [below for top, below in state.on.items() if top == disk][0]
	new_below = state.top[dest]
	if(disk_size == 1):
		return [('move_disk', disk, below, new_below, source, dest)]
	else:
		return [('hanoi_sub', disk_size - 1, source, via, dest), 
				('move_disk', disk, below, new_below, source, dest),
				('hanoi_sub', disk_size - 1, via, dest, source)]
				
pyhop.declare_methods('hanoi_sub', hanoi_sub)
