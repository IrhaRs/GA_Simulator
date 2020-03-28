import pygame
from pygame.locals import *
import sys
import random

class PygameWindow:
    def __init__(self, w=1280, h=720, title="Pygame_window"):
        pygame.init()
        self.game_running = True
        #setup fps
        self.fps = 30
        self.fps_clock = pygame.time.Clock()

        #setup width/height
        self.width = w
        self.height = h
        #make display
        self.background_color = (0, 0, 0)
        self.display = pygame.display.set_mode((self.width, self.height))
        self.title = title
        pygame.display.set_caption(self.title)
        

        #objects
        self.env = None
        #variables

        print(f"made {self.title}")

    def game_loop(self):
        while self.game_running:
            #set bg
            self.display.fill(self.background_color)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_running = False
                
            
            #####################################################################################################
            #Update
            self.env.update()

            #check collisions
            self.env.collisions()    
            # Draw.
            self.env.draw(self.display)

            pygame.display.flip()
            self.fps_clock.tick(self.fps)

        pygame.display.quit()
        pygame.quit()
        sys.exit(1)
    
    def run(self):
        self.game_loop()
    
    def load_env(self, env):
        self.env = env
