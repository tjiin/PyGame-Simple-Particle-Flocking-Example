import pygame
from pygame.locals import *
import random
import math
import numpy as np
from pprint import *

# CONTROL CONSTANTS
max_speed = 30
num_particles = 20
neighbour_distance = 500
desired_separation = 100
desired_neighbours = 20
separation_weight = 1.0
cohesion_weight = 1.0
alignment_weight = 1.0

BLACK = (0,0,0)
WHITE = (255,255,255)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, color, radius):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.image = pygame.Surface([radius*2, radius*2])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.pos = pygame.draw.circle(self.image, color, [radius,radius], radius)
        self.pos.x = x
        self.pos.y = y
        self.dx = self.dy = 0
        self.vel = [self.dx, self.dy]
        self.mass = 5

    def move(self):

        # Get accel from forces
        separation_accel = self.calc_separation_accel()
        cohesion_accel = self.calc_cohesion_accel()
        alignment_accel = self.calc_alignment_accel()

        accelx = sum( [separation_accel[0], cohesion_accel[0], alignment_accel[0] ])
        accely = sum( [separation_accel[1], cohesion_accel[1], alignment_accel[1] ])

        # Add accel to velocity
        self.dx = limit( self.dx + accelx, max_speed )
        self.dy = limit( self.dy + accely, max_speed )

        # Add velocity to position
        self.pos = self.pos.move(self.dx, self.dy) 

        # Boundaries
        if( self.pos.left < 0 or self.pos.right > sw ):
            self.dx = -self.dx
            self.pos.x += self.dx
        if( self.pos.top < 0 or self.pos.bottom > sh ):
            self.dy = -self.dy
            self.pos.y += self.dy

    # Alignment

    def calc_alignment_accel(self):
        neighbour_count = 0
        avg_vel = [0,0]
        for i,b in enumerate(objects):
            dist = obj_dist(self,b)
            if( dist < neighbour_distance and dist > 0 ):
                avg_vel[0] += b.dx
                avg_vel[1] += b.dy
                neighbour_count += 1
        if( neighbour_count > 0 and sum(avg_vel) != 0 ):
            avg_vel = [ x/float(neighbour_count) for x in avg_vel ]
            avg_vel = [ x*max_speed for x in norm(avg_vel[0], avg_vel[1]) ]
            accelx = (avg_vel[0] - self.dx) / self.mass * alignment_weight 
            accely = (avg_vel[1] - self.dy) / self.mass * alignment_weight          
            return( [accelx, accely] )
        return( [0,0] )

    # Cohesion

    def calc_cohesion_accel(self):
        neighbour_count = 0
        avg = [0,0]
        for i,b in enumerate(objects):
            dist = obj_dist(self,b)
            if( dist < neighbour_distance and dist > 0 ):
                avg[0] += b.pos.x
                avg[1] += b.pos.y
                neighbour_count += 1
        if( neighbour_count > 0 ):
            avg = [ x/float(neighbour_count) for x in avg ]
            sign = 1 # normal
            if( neighbour_count > desired_neighbours ):
                sign = -1
            try:
                diff = [ max_speed * x for x in norm( (avg[0]-self.pos.x)*sign, (avg[1]-self.pos.y)*sign ) ] # mag might be 0
                accelx = (diff[0] - self.dx) / self.mass * cohesion_weight 
                accely = (diff[1] - self.dy) / self.mass * cohesion_weight           
                return( [accelx, accely] )
            except:
                pass
        return([0,0])
    
    # Separation
    
    def calc_separation_accel(self):
        separate_count = 0
        steerx = 0
        steery = 0
        for i,b in enumerate(objects):
            dist = obj_dist(self,b)
            if( dist < desired_separation and dist > 0 ):
                diffx = self.pos.x - b.pos.x
                diffy = self.pos.y - b.pos.y
                m = mag(diffx, diffy)
                diffx = diffx/m/dist # normalze + weight by distance
                diffy = diffy/m/dist
                steerx += diffx
                steery += diffy
                separate_count += 1

        if( separate_count > 0 and steerx*steery != 0 ):
            steerx = steerx / float(separate_count)
            steery = steery / float(separate_count)
            m = mag(steerx, steery)
            steerx = steerx/m * max_speed # normalize + multiply by max_speed
            steery = steery/m * max_speed
            accelx = (steerx - self.dx) / self.mass * separation_weight 
            accely = (steery - self.dy) / self.mass * separation_weight

            return( [accelx, accely] )
        
        return( [0,0] )

def random_color():
    return( [ random.random()*255 for i in range(3) ] )

def obj_dist(a,b):
    return( mag(a.pos.x - b.pos.x, a.pos.y - b.pos.y) )

def mag(x,y):
    return( math.sqrt( pow(x,2) + pow(y,2) ) )

def norm(x,y):
    m = mag(x,y)
    return( [x/m, y/m] )

def limit(x, maximum):
    if( x < maximum ):
        return(x)
    else:
        return(maximum)

# Pygame init
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
sw = screen.get_size()[0]
sh = screen.get_size()[1]
background = pygame.Surface(screen.get_size())
background.fill(WHITE)
screen.blit(background, (0, 0))

objects = []
for i in range(num_particles):
    x = random.uniform(20,sw-20)
    y = random.uniform(20,sh-20)
    b = Ball(x, y, random_color(), 10)
    objects.append(b)

while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            break
        
    for b in objects:
        screen.blit(background, b.pos) # clear sprites
    for b in objects:
        b.move()
        screen.blit(b.image, b.pos)
        
    pygame.display.update()
    pygame.time.delay(25)

pygame.quit()

print('Done')
