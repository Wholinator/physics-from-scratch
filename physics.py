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

    def to_cartesian(self):
        return cartesian_coord(
            self.r * math.cos(self.theta),
            self.r * math.sin(self.theta)
        )

    def __add__(self, p):
        if isinstance(p, polar_coord):
            r = math.sqrt(
                math.pow(self.r, 2) + math.pow(p.r, 2) + 
                (2 * self.r * p.r * math.cos(p.theta - self.theta))
            )
            theta = self.theta + math.atan(
                (p.r * math.sin(p.theta - self.theta)) / 
                (self.r + (p.r * math.cos(p.theta - self.theta)))
            )
            return polar_coord(r=r, theta=theta)
        if isinstance(p, cartesian_coord):
            raise TypeError("Attempting to add polar and cartesian, please convert to desired format first")

        # just throw the error if all else fails
        return self + p

    # the mathed out __add__ function above is 60% faster than this
    def add_slow(self, p):
        # convert back and forth, let's see
        if isinstance(p, polar_coord):
            return (self.to_cartesian() + p.to_cartesian()).to_polar()

        # all else fails, just throw the exception
        return self + p



class cartesian_coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, p):
        if isinstance(p, cartesian_coord):
            return cartesian_coord(
                self.x + p.x,
                self.y + p.y
            )
        if isinstance(p, polar_coord):
            raise TypeError("Please convert coordinates to same type")
        raise TypeError("Cannot add cartesian_coord to " + type(p))

    def to_polar(self):
        return polar_coord(
            r = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2)),
            theta = math.atan2(self.y, self.x)
        )

class circle():
    def __init__(self, canvas, mass, position,
            velocity=cartesian_coord(0,0), acceleration=cartesian_coord(0,0), momentum=cartesian_coord(0,0), 
                    energy=0, charge=0, color="orange"):
        self.mass = mass
        self.position = position
        self.movement = cartesian_coord(0, 0)
        self.velocity = velocity
        self.acceleration = acceleration
        self.momentum = momentum
        self.energy = energy
        self.charge = charge
        self.size = 10 # set to minimum then math.log then max
        
        # drawing stuff
        self.start_point = cartesian_coord(
            position.x - (self.size / 2),
            position.y - (self.size / 2)
        )
        self.end_point = cartesian_coord(
            position.x + (self.size / 2),
            position.y + (self.size / 2)
        )
        self.canvas = canvas
        self.vis = self.canvas.create_oval(
            self.start_point.x,
            self.start_point.y,
            self.end_point.x,
            self.end_point.y,
            fill=color
        )


    def move(self):
        self.canvas.move(self.vis, self.movement.x, self.movement.y)

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

# hmmmmm this just feels wrong to do, but how else could I accurately get 
# position change for the graphics? Would I just wave the positions of everything
# and then calculate the change and apply that? I'm trying to ensure smallest 
# possible error accumulation... accurate display.
#
# I could just place a quick error check on positions every 100 iterations and erase/redraw
# if the positions get out of hand. It's probably useful to somehow record the difference
# between displayed position and physics position somewhere to keep track of if this is even an issue
def calc_position_change(velocity, time_delta):
    return cartesian_coord(
        velocity.x * time_delta,
        velocity.y * time_delta
    )

def calc_position(circle, pos_delta):
    return cartesian_coord(
        circle.position.x + pos_delta.x,
        circle.position.y + pos_delta.y
    )

# do these in a row or calculate changes and apply all at once?
def tick_object_row(circle, force, delta):
    circle.acceleration = calc_acceleration(circle, force)
    circle.velocity = calc_velocity(circle, circle.acceleration, delta)
    circle.movement += calc_position_change(circle.velocity, delta)
    circle.position = calc_position(circle, circle.movement)

def tick_object_simult(circle, force, delta):
    acceleration = calc_acceleration(circle, force)
    velocity = calc_velocity(circle, circle.acceleration, delta)
    movement = calc_position_change(circle.velocity, delta)
    position = calc_position(circle, movement)

    circle.acceleration, circle.velocity, circle.position  = acceleration, velocity, position
    circle.movement += movement # += to add up changes until next visual frame

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
# background
canvas.create_rectangle(0, 0, x_max, y_max, fill="black")


# iterates and draws masses
# could be expanded to draw arrows or all kinds of things!
def draw():
    # TODO: transition this to move rather than paint over!

    # TODO: add velocity arrows
    # TODO: add hollow spheres at edge of square when circle goes out of bounds
    # TODO: Change color with mass
    # TODO: change size with mass by log or something
    # call physics changes, could alter iteration inside from 1 to 10, hopefully it runs well enough
    physics()
    for cir in masses:
        cir.move()
        
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
    masses.append(circle(canvas, 150000000, cartesian_coord(15, 15)))
    masses.append(circle(canvas, 1, cartesian_coord(150, 150)))
    masses.append(circle(canvas, 5000, cartesian_coord(140, 160)))
    draw()


if __name__ == "__main__":
    start(event=None)
    # window.bind('<Return>', start)
    window.mainloop()


#TODO IDEAS:
# verify conservation of momentum: maybe add text to display total momentum to gui
# same with total energy I guess

# add collision to bind two objects together, maybe merge them into a single object at collision

# add more data to display, possibly escape velocity color change