from objects import PygameWindow, Environment
import os

class GA_Simulator:
    def __init__(self):
        #clear terminal
        os.system('cls')
        #create pygame window
        self.window = PygameWindow.PygameWindow(1280, 720, "Genetic Algorithm Simulator")
        
        #create instance of Enviroment
        self.ENV = Environment.Environment()
        #load example 1
        self.ENV.load_example_env1()
        #make population
        self.ENV.new_population()
        self.window.fps = 120
        #add env to window
        self.window.load_env(self.ENV)
        self.run()

    def run(self):
        self.window.run()

GA_Simulator()



