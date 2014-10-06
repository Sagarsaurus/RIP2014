from pyhop import *
import hanoi_domain

state = State('hanoi-state')
state.disk = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10']
state.top = {'p1':'p1', 'p2':'p2', 'p3':'d1'}
state.size = {'d1':1, 'd2':2, 'd3':3, 'd4':4, 'd5':5, 'd6':6, 'd7':7, 'd8':8, 'd9':9, 'd10':10, 'd11':11, 'd12':12
              'p1':12, 'p2':12, 'p3':12}
state.on = {'d1':'d2', 'd2':'d3', 'd3':'d4', 'd4':'d5', 'd5':'d6', 'd6':'d7', 'd7':'d8', 'd8':'d9', 'd9':'d10', 'd10':'d11', 'd11':'d12','d12':'p3'}
pyhop(state, [('hanoi_sub', 12, 'p1', 'p3', 'p2')], verbose=1)
