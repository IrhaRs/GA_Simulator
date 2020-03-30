from objects import Actor, ActionObject as ActObj
from lib import Collision,ga
import random

"""
Environment: creates maps and manages collision etc
"""
class Environment:
    def __init__(self, w=1280, h=720, actor_amount = 1000):
        #variables
        self.lst_obstacles = []
        self.lst_actors = []
        self.actor_amount = actor_amount
        self.generation = 0
        self.mutation_rate = 20

        self.w = w
        self.h = h

    def update(self):
        #update all the objects and actors
        [obstacle.update() for obstacle in self.lst_obstacles]
        [actor.update() for actor in self.lst_actors]

        

    def collisions(self):
        #collision for all the objects and actors
        for obstacle in self.lst_obstacles:
            if not isinstance(obstacle, ActObj.Start):
                for actor in self.lst_actors:
                    if not actor.dead:
                        if Collision.AABB_Collision_rect(obstacle.AABB_rect(), actor.AABB_rect()):
                            if Collision.Circle_Rect_Collision2(actor.collision(), obstacle.collision()):
                                obstacle.action_function(actor)
        
        #if all actors are dead go to new generation
        amount_dead = len([x for x in self.lst_actors if x.dead])
        if amount_dead >= self.actor_amount:
            self.new_generation()
                

    def draw(self, surface):
        #draw all the objects and actors
        [obstacle.draw(surface) for obstacle in self.lst_obstacles]
        [actor.draw(surface) for actor in self.lst_actors]

    def new_population(self):
        #make a new population of actors
        for i in range(self.actor_amount):
            startpos = self.get_startposition()
            goalpos = self.get_goalposition()
            a = Actor.Actor(startpos[0], startpos[1], goalpos[0], goalpos[1])
            a.brain_length=500
            a.create_brain()
            self.lst_actors.append(a)
        
    def get_startposition(self):
        #find a start if not found default window/2
        lst_start = [obstacle for obstacle in self.lst_obstacles if isinstance(obstacle, ActObj.Start)]
        area = (self.w/2, self.h/2, 0,0)
        if len(lst_start) > 0: 
            area = random.choice(lst_start).collision()

        #pick random spot in the area
        x = random.randint(area[0], area[0]+area[2])
        y = random.randint(area[1], area[1]+area[3])

        return (x, y)

    def get_goalposition(self):
        #find a goal if not found default window/2
        lst_goal = [obstacle for obstacle in self.lst_obstacles if isinstance(obstacle, ActObj.Goal)]
        area = (self.w-round(self.w/30)-20, self.h/2, 0, 0)
        if len(lst_goal) > 0: 
            area = random.choice(lst_goal).collision()

        #calc middle of goal
        x = area[0]+round(area[2]/2)
        y = area[1]+round(area[3]/2)

        return (x, y)

    def load_example_env1(self):
        #create start
        self.lst_obstacles.append(ActObj.Start(round(self.w/30), round(self.h/2),0,0))
        #create goal
        self.lst_obstacles.append(ActObj.Goal(self.w-round(self.w/30)-50, round(self.h/2)-25, 50,50))
        #add borders
        self.lst_obstacles.append(ActObj.Lava(-10, -10, self.w+(2*11), 11)) #top
        self.lst_obstacles.append(ActObj.Lava(-10, self.h-1, self.w+(2*11), 11)) #bottom
        self.lst_obstacles.append(ActObj.Lava(-10, -10, 11, self.h+(2*11))) #left
        self.lst_obstacles.append(ActObj.Lava(self.w-1, -10, 11, self.h+(2*11))) #right

    def new_generation(self):
        #make new generation~
        self.generation += 1

        sorted_fitness = ga.sort_fitness(self.lst_actors)                                               #sorted by fitness
        ga.print_stats(self.generation, sorted_fitness)                                                 #print stats                                               
        parents = sorted_fitness[:round(len(sorted_fitness)/2)]                                         #slice first half
        children = [Actor.crossover(*ga.select_parents(parents)) for x in range(round(len(parents)))]   #crossover make new children
        [child.mutate(self.mutation_rate) for child in children]                                        #mutate the children
        parents = [parent.copy() for parent in parents]                                                 #reset parents
        new_pop = parents + children                                                                    #form new population
        self.lst_actors = new_pop
        if self.generation%5 == 0:
            self.mutation_rate-=self.mutation_rate/5
            print(f"Mutation rate changed to: {self.mutation_rate}")


def test():
    e = Environment()
    e.actor_amount=5
    e.lst_obstacles.append(ActObj.Start(30,30,5,5))
    e.new_population()
    print([a.collision() for a in e.lst_actors])
    print("------------")
    print(e.get_startposition())

