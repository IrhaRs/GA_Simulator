from objects import Actor, ActionObject as ActObj
from lib import 
import random

"""
Environment: creates maps and manages collision etc
"""
class Environment:
    def __init__(self, w=1280, h=720, actor_amount = 100):
        #variables
        self.lst_obstacles = []
        self.lst_actors = []
        self.actor_amount = actor_amount

        self.w = w
        self.h = h

    def update(self):
        #update all the objects and actors
        [obstacle.update() for obstacle in self.lst_obstacles]
        [actor.update() for actor in self.lst_actors]

    def collisions(self):
        #collision for all the objects and actors
        pass

                

    def draw(self, surface):
        #draw all the objects and actors
        [obstacle.draw(surface) for obstacle in self.lst_obstacles]
        [actor.draw(surface) for actor in self.lst_actors]

    def new_population(self):
        #make a new population of actors
        for i in range(self.actor_amount):
            startpos = self.get_startposition()
            a = Actor.Actor(startpos[0],startpos[1])
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

def test():
    e = Environment()
    e.actor_amount=5
    e.lst_obstacles.append(ActObj.Start(30,30,5,5))
    e.new_population()
    print([a.collision() for a in e.lst_actors])
    print("------------")
    print(e.get_startposition())
