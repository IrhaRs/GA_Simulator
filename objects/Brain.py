import numpy as np
import random
import math

"""
Brain: vector path for the actors.
"""
class Brain:
    def __init__(self, length=500):
        self.length=length
        self.lst_vectors = []
        self.path = iter(self.lst_vectors)
        self.max = 10
        self.steps_done = 0
        
    def create_brain(self):
        [self.lst_vectors.append(self.random_vector()) for x in range(self.length)]
        self.path = iter(self.lst_vectors)

    def next_step(self):
        self.steps_done+=1
        return next(self.path, None)

    def random_vector(self):
        return [round((random.random()*(self.max*2)) - self.max),round((random.random()*(self.max*2))- self.max)] 


def test():
    b = Brain(5)
    b.create_brain()
    print(b.lst_vectors)
    print("----------")
    while True:
        answer = b.next_step()
        if answer is not None: 
            print(answer)
        else: break

