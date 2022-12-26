import physics
import random
import math
import timeit

# this is to time the 2 addition methods for polar coordinates
# I've forgotten what I was even doing it for but that's how it goes ya know?



# create coords list
setup = '''
import physics
import random
import math
N = 100
coords = []
for i in range(0, N):
    coords.append(
        physics.polar_coord(
            r = random.random() * 8,
            theta = random.random() * math.pi
        )
    )
'''
stmt1 = '''
for i in range(0, N-1):
    coords[i].add_1(coords[i+1])
'''

stmt2 = '''
for i in range(0, N-1):
    coords[i].add_2(coords[i+1])
'''
#stmt1@10000:N=100 ::: 4.08, 4.37, 4.71, 4.50, 4.44
#stmt2@10000:N=100 ::: 2.56, 2.59, 2.64, 2.71, 2.64
# yooooooo, the math heavy addition, is drastically faster,
# probably because it doesn't need to create classes
f = timeit.timeit(stmt=stmt2, setup=setup, number = 10000)
print(f)