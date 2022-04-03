import numpy as np
import numpy as np
import networkx as nx
import random as ra
import matplotlib.pyplot as plt
import math 


def simulation_marriage_market(n_men, n_women, d_men, d_women):
    '''
    Function that generates a marriage problem instance
    INPUTS:
        n_men: number of men in the market
        n_women: number of women in the market
        d_men: size of preference list of man for women
        d_women: size of preference list of women for men
    Outputs:
        men: list of men in the market
        women: list of women in the market
        men_preferences: dictionary with preferences list per man in the market
        women_preferences: dictionary with preferences list per woman in the market
    '''

    men = [i for i in range(n_men)]
    women = [i for i in range(n_women)]

    men_preferences = {}
    women_preferences = {}

    for man in men: 
        men_preferences[man] = np.random.choice(women, d_men).tolist()

    for woman in women:
        women_preferences[woman] = np.random.choice(men, d_women).tolist()
    
    return men, men_preferences, women, women_preferences

men, men_prefereces, women, women_preferences = simulation_marriage_market(10, 10, 10, 2)

print(men)
print(women)
print(men_prefereces)
print(women_preferences)

print('code succesfull')