import numpy as np
import random
"""
genetic algorithm methods made for the GA_simulator
"""
def print_stats(gen_num, lst):
    #print out information about current generation
    best = lst[0]
    worst = lst[-1]
    avg = total_fitness(lst)/len(lst)
    print(f"Generation: {gen_num} | avg: {avg} | best: {best.fitness} | worst: {worst.fitness}")

def sort_fitness(lst):
    #assumes lst items have .fitness
    lst_sorted = sorted(lst, key= lambda x: x.fitness ,reverse=True)
    return lst_sorted

def select_parents(weighted_lst):
    total_fit = total_fitness(weighted_lst)
    if total_fit != 0:
        selection_probs = [c.fitness/total_fit for c in weighted_lst]
        parent1=  weighted_lst[np.random.choice(len(weighted_lst), p=selection_probs)]
        parent2=parent1
        while parent1 is parent2:
            parent2 = weighted_lst[np.random.choice(len(weighted_lst), p=selection_probs)]
        return (parent1, parent2)
    else:
        return (random.choice(weighted_lst),random.choice(weighted_lst))

def total_fitness(lst):
    return sum([x.fitness for x in lst])