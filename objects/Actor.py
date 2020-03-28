import pygame
from objects import Brain

"""
Actor: little dot that tries to solve the map
"""
class Actor():
    def __init__(self, x=0, y=0, size=5, brain = None):
        #variables
        self.x = x
        self.y = y
        self.size = size
        self.color = (255,255,255)
        
        #brain
        self.brain = brain
        self.brain_length = 500

        #fitness/genetic algorithm things
        self.fitness = 0
        self.steps_taken = 0
        self.dead = False

        #debug variables
        self.debug = False
        self.AABB_rect_padding = 10

    

    def AABB_rect(self):
        #return the AABB rect around the circle with padding.
        return ((self.x-(self.size/2))-self.AABB_rect_padding, (self.y-(self.size/2))-self.AABB_rect_padding, self.size+(2*self.AABB_rect_padding), self.size+(2*self.AABB_rect_padding))

    def collision(self):
        #return the circle collision variable.
        return (self.x, self.y, self.size)

    def update(self):
        #executes next brains step
        if not self.dead:
            step = self.brain.next_step()
            if step is not None:
                self.x += step[0]
                self.y += step[1]
            else:
                self.dead=True


    def draw(self, surface):
        #draw on the screen:
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)

        if self.debug:
            #draw AABB
            pygame.draw.rect(surface, (0,220,0), self.AABB_rect())

    def create_brain(self):
        self.brain= Brain.Brain(self.brain_length)
        self.brain.create_brain()



