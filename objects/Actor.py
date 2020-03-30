import pygame
import itertools 
from objects import Brain
from lib import Collision
import copy


"""
Actor: little dot that tries to solve the map
"""
class Actor():
    def __init__(self, x=0, y=0, goalx=10, goaly=10, size=5, brain = None):
        #variables
        self.title = "Actor"
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.size = size
        self.color = (255,255,255)
        
        #brain
        self.brain = brain
        self.brain_length = 500

        #fitness/genetic algorithm things
        self.fitness = 0
        self.goal_x = goalx
        self.goal_y = goaly
        self.steps_taken = 0
        self.goal_reward = 50000
        self.dead = False
        self.reach_goal = False

        #debug variables
        self.debug = False
        self.AABB_rect_padding = 10

    def __repr__(self):
        return f"{self.title}"

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
                self.steps_taken+=1
            else:
                self.die()
                




    def draw(self, surface):
        #draw on the screen:
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)

        if self.debug:
            #draw AABB
            pygame.draw.rect(surface, (0,220,0), self.AABB_rect(),1)

    def create_brain(self):
        self.brain= Brain.Brain(self.brain_length)
        self.brain.create_brain()

    def die(self):
        self.dead = True
        self.fitness = self.calculate_fitness()

    def goal(self):
        self.reach_goal = True

    def calculate_fitness(self):
        #points per step: 10   (max points = brain_length * 10 = 5000)
        #points for distance to goal: goal_reward/(distance to goal)  (max points = 50000)
        #points for hitting goal with less steps: (brain_length - steps_taken) * (30)  (example points = 500-70 *30 = 12000)

        fitness = 0
        fitness += self.steps_taken * 10
        dist = (Collision.Distance_Line(self.x, self.y, self.goal_x, self.goal_y))
        if dist == 0:
            fitness += self.goal_reward
        else:
            fitness += self.goal_reward/dist
        if self.reach_goal:
            fitness += (self.brain_length-self.steps_taken) * 30
        return fitness
    
    def mutate(self, rate):
        self.brain.mutate(rate)


    def copy(self):
        new_brain = Brain.Brain(self.brain_length)
        new_brain.brain_from_lst(self.brain.lst_vectors)
        return  Actor(self.start_x, self.start_y, self.goal_x, self.goal_y, self.size, new_brain)

def crossover(actor1, actor2):
    #make sure the highest fitness is always first
    
    highest=None
    lowest=None
    if actor1.fitness > actor2.fitness:
        highest = actor1
        lowest = actor2
    else:
        highest = actor2
        lowest = actor1
    #make new brain by taking the first item and alternating picking from the two parents
    crossover_lst_vectors = list(itertools.chain(*zip(highest.brain.lst_vectors[::2], lowest.brain.lst_vectors[1::2])))
    new_brain = Brain.Brain(len(crossover_lst_vectors))
    new_brain.brain_from_lst(crossover_lst_vectors)
    #get the x and y
    

    child = Actor(highest.start_x, highest.start_y, highest.goal_x, highest.goal_y, highest.size, new_brain)

    return child

