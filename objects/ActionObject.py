import pygame


"""
parent class for all the obstacles in the game
"""
class Action_Object:
    def __init__(self, x=0, y=0, w=20, h=20, title="Action_Object"):
        #variables
        self.title = title
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = (255,255,255)

        #debug variables
        self.debug = False
        self.AABB_rect_padding = 10
    
    def __str__(self):
        return self.title

    def __repr__(self):
        return f"obstacle: {self.title}"

    def action_function(self, actor):
        #happens when someone collides with the object.
        if self.debug:
            print(f"{str(actor)} interacted with {str(self)}")

    def AABB_rect(self):
        #rectangle to activate collision calculations
        return (self.x-(self.AABB_rect_padding), self.y-(self.AABB_rect_padding), self.w+(2*self.AABB_rect_padding), self.h+(2*self.AABB_rect_padding))

    def collision(self):
        #gives the collisionbox
        return (self.x, self.y, self.w, self.h)
    
    def update(self):
        #update on every cycle
        pass

    def draw(self, surface):
        #draw on the screen: collision = the area need to be shown on screen
        pygame.draw.rect(surface, self.color, self.collision())

        if self.debug:
            #draw AABB
            pygame.draw.rect(surface, (0,220,0), self.AABB_rect(),1)
    
    



"""
Goal: Final goal for the game actors to reach.
"""
class Goal(Action_Object):
    def __init__(self, x=0, y=0, w=20, h=20):
        super().__init__(x, y, w, h,"Goal")
        self.color = (8, 168, 24)

    def action_function(self, actor):
        super().action_function(actor)
        #give points based on the amount of steps it took compared to the max amount of steps he could do.
        #set variable to stop taking new steps (completed?)
        actor.goal()
        actor.die()


"""
Lava: instant death on touch, fitness score doesnt increase
"""
class Lava(Action_Object):
    def __init__(self, x=0, y=0, w=20, h=20):
        super().__init__(x, y, w, h, "Lava")
        self.color = (184, 46, 4)

    def action_function(self, actor):
        super().action_function(actor)
        #set variable to stop taking new steps (completed/dead?)
        actor.die()


"""
Start:  set the area where dots can start to spawn
        slightly bigger area means that the dots have to take the optimal path to not hit anything
        if later made smaller would result in best path (?)
"""
class Start(Action_Object):
    def __init__(self, x=0, y=0, w=20, h=20):
        super().__init__(x, y, w, h, "Start")
        self.color = (85, 92, 201)
    
"""
Wall: Static collision, cant pass through.
"""
class Wall(Action_Object):
    def __init__(self, x=0, y=0, w=20, h=20):
        super().__init__(x, y, w, h, "Wall")
        self.color = (123, 97, 135)

    def action_function(self, actor):
        super().action_function(actor)
        #set actor back to collide with the wall. (static collision)
        #TODO
    

"""
Food:   Eat food to get more fitness :) 
        (acts as checkpoints kinda hopefully)
"""
class Food(Action_Object):
    def __init__(self, x=0, y=0, w=20, h=20, food_amount= 20):
        super().__init__(x, y, w, h, "Wall")
        self.color = (123, 97, 135)
        self.food_amount = food_amount

    def action_function(self, actor):
        super().action_function(actor)
        #give actor more fitness per food.
        #TODO