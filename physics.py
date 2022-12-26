import math
import tkinter as tk
from scipy import constants

# physics
x_max = 500
y_max = 500

# objects with:
    # mass
    # position
    # velocity
    # acceleration
    # momentum
    # energy
    # # charge

# could just combine these and auto update whenever either is changed but that would probably be
# just a bunch of unnecessary computation
class polar_coord():
    def __init__(self, r, theta):
        self.r = r
        self.theta = theta

class cartesian_coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class circle():
    def __init__(self, mass, position,
            velocity=cartesian_coord(0,0), acceleration=cartesian_coord(0,0), momentum=cartesian_coord(0,0), 
                    energy=0, charge=0):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.momentum = momentum
        self.energy = energy
        self.charge = charge
        self.size = 10 # set to minimum then math.log then max

# returns distance vector with pythagorean distance and radian angle
def difference_polar(point_from, point_to):
    x_dist = point_to.x - point_from.x
    y_dist = point_to.y - point_from.y
    distance = math.sqrt(math.pow(x_dist, 2) + math.pow(y_dist, 2))
    direction = math.atan2(y_dist, x_dist)

    return polar_coord(distance, direction)

# gravitational force
def calc_gravitational_force(circle_from, circle_to):
    diff = difference_polar(circle_from.position, circle_to.position)
    force = (constants.G * circle_from.mass * circle_to.mass) / math.pow(diff.r, 2)

    return cartesian_coord(
        force * math.cos(diff.theta),
        force * math.sin(diff.theta)
    )

def calc_acceleration(circle, force):
    return cartesian_coord(
        (force.x / circle.mass),
        (force.y / circle.mass)
    )

def calc_velocity(circle, acceleration, time_delta):
    return cartesian_coord(
        circle.velocity.x + (acceleration.x * time_delta),
        circle.velocity.y + (acceleration.y * time_delta)
    )

def calc_position(circle, velocity, time_delta):
    return cartesian_coord(
        circle.position.x + (velocity.x * time_delta),
        circle.position.y + (velocity.y * time_delta)
    )

# do these in a row or calculate changes and apply all at once?
def tick_object_row(circle, force, delta):
    circle.acceleration = calc_acceleration(circle, force)
    circle.velocity = calc_velocity(circle, circle.acceleration, delta)
    circle.position = calc_position(circle, circle.velocity, delta)

def tick_object_simult(circle, force, delta):
    acceleration = calc_acceleration(circle, force)
    velocity = calc_velocity(circle, circle.acceleration, delta)
    position = calc_position(circle, circle.velocity, delta)

    circle.acceleration, circle.velocity, circle.position = acceleration, velocity, position

# force of:
    # gravity
    # E&M

# start with circle
# get canvas
# show object in location
    # convert object position to canvas position
    # calculate size from mass
    # center circle on position

# apply forces
    # position from velocity from acceleration from force from field

# play loop
    # time steps: and time step resolution
    # calculate fields from objects
    # calculate forces from fields
    # calculate acceleration from force
    # calculate velocity from acceleration
    # calculate position from velocity
    # # is there a better way to do this?

    # can be done as all forces then all acc
    # or calculate all fields then apply them one at a time


### separate into functions, namely
### have 2 parallel things going, a physics simulation running
#       continuously in the while true loop (maybe add a pause button for stop start)
### and a drawing loop that just runs at a certain framework and takes whatever
#       list of objects exists, and draws them continuously using the tkinter after function
### and apparently after those 2 function calls we need a mainloop call I think, we'll see


DELTA = 50
TOTAL = 0

# create objects and place in array
masses = []

window = tk.Tk()
canvas = tk.Canvas(window, width=x_max, height=y_max)
canvas.pack()

# iterates and draws masses
# could be expanded to draw arrows or all kinds of things!
def draw():
    # TODO: transition this to move rather than paint over!

    # TODO: add velocity arrows
    # call physics changes, could alter iteration inside from 1 to 10, hopefully it runs well enough
    physics()
    canvas.create_rectangle(0, 0, x_max, y_max, fill="black")
    for cir in masses:
        size = cir.size
        position = cir.position
        p1 = cartesian_coord(
            position.x - (size / 2),
            position.y - (size / 2)
        )
        p2 = cartesian_coord(
            position.x + (size / 2),
            position.y + (size / 2)
        )
        canvas.create_oval(p1.x, p1.y, p2.x, p2.y, fill="orange")

    window.after(10, draw)

#### this is the actual physics simulation 
# sets up a force matrix to contain active forces
# begins a continuous loop to update the masses by
# # # calculating new force matrix from gravitational fields
# # # update mass metrics with force matrix
#
# the idea is this runs parallel to the graphics updates so that graphics framerate
# is not tied to physics framerate but it should be possible to tie it by removing
# graphics framerate .after function and just placing the draw call inside this loop
def physics():
    dim = len(masses)
    # construct force matrix
    force_matrix = [[cartesian_coord(0, 0) for i in range(dim)] for j in range(dim)]
    global TOTAL

    # while True:
    for ikj in range(0, 1):
        TOTAL += DELTA
        # so I could calculate the change for every other object, for every object,
        # but with equivalent mass/charges the magnitude of force is identical but in
        # opposite direction, it might be worth making an array of force interactions and
        # simply updating the new forces each tick, multiple dimensions for types of forces, etc.
        for i in range(0, dim):
            for j in range(0, dim):
                if i == j:
                    continue

                force_matrix[i][j] = calc_gravitational_force(circle_from=masses[i], circle_to=masses[j])
        
        # update all metrics
        for i in range(0, dim):
            obj = masses[i]
            # sum forces for obj
            sum_force = cartesian_coord(
                sum([force.x for force in force_matrix[i]]),
                sum([force.y for force in force_matrix[i]])
            )
            
            tick_object_row(obj, sum_force, DELTA)


    # update graphics here to tie framerate 

def start(event):
    masses.append(circle(150000000, cartesian_coord(15, 15)))
    masses.append(circle(1, cartesian_coord(150, 150)))
    masses.append(circle(5000, cartesian_coord(140, 160)))
    draw()

start(event=None)
# window.bind('<Return>', start)
window.mainloop()


#TODO IDEAS:
# verify conservation of momentum: maybe add text to display total momentum to gui
# same with total energy I guess

# add collision to bind two objects together, maybe merge them into a single object at collision

# add more data to display, possibly escape velocity color change