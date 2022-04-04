import numpy as np
import numpy as np
import networkx as nx
import random as ra
import matplotlib.pyplot as plt
import math 


def simulationMarriageMarket(n_men, n_women, d_men, d_women):
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
        if n_women < d_men:
            men_preferences[man] = np.random.choice(women, n_women, replace=False).tolist()
        else:
            men_preferences[man] = np.random.choice(women, d_men, replace=False).tolist()

    for woman in women:
        if n_men < d_women:
            women_preferences[woman] = np.random.choice(men, n_men, replace=False).tolist()
        else:
            women_preferences[woman] = np.random.choice(men, d_women, replace=False).tolist()
    
    return men_preferences, women_preferences

def galeShapley(n_men, n_women, men_preferences, women_preferences):
    
    # Initially, all n men are unmarried
    unmarried_men = list(range(n_men))
    print(unmarried_men)
    # None of the men has a spouse yet, we denote this by the value None
    man_spouse = [None] * n_men                      
    # None of the women has a spouse yet, we denote this by the value None
    woman_spouse = [None] * n_women                     
    # Each man made 0 proposals, which means that 
    # his next proposal will be to the woman number 0 in his list
    next_man_choice = [0] * n_men
    
    # The size of the preference lists of the proposing side
    size_preferences = len(men_preferences[0])
                           
    #This is the total number of possible proposals before all men go through their full preference lists
    total_posible_proposals = size_preferences * n_men

    # While there exists at least one unmarried man or there are men with possible proposals still available:
    while unmarried_men and (sum(next_man_choice)<= total_posible_proposals):
        # Pick an arbitrary unmarried man
        he = unmarried_men[0]

        while next_man_choice[he]>=size_preferences:
            unmarried_men.pop(0)
            he = unmarried_men[0]                     
        # Store his ranking in this variable for convenience
        his_preferences = men_preferences[he]       
        # Find a woman to propose to
        she = his_preferences[next_man_choice[he]] 
        # Store her ranking in this variable for convenience
        her_preferences = women_preferences[she]
        # Find the present husband of the selected woman (it might be None)
        current_husband = woman_spouse[she]
        
        # Now "he" proposes to "she". 
        # Decide whether "she" accepts, and update the following fields
        # 1. manSpouse
        # 2. womanSpouse
        # 3. unmarriedMen
        # 4. nextManChoice
        if current_husband == None:
          #No Husband case
          #"She" accepts any proposal
          woman_spouse[she] = he
          man_spouse[he] = she
          #"His" nextchoice is the next woman
          #in the hisPreferences list
          next_man_choice[he] = next_man_choice[he] + 1
          #Delete "him" from the 
          #Unmarried list
          unmarried_men.pop(0)

        else:
          #Husband exists
          #Check the preferences of the 
          #current husband and that of the proposed man's
          current_index = her_preferences.index(current_husband)
          his_index = her_preferences.index(he)
          #Accept the proposal if 
          #"he" has higher preference in the herPreference list
          if current_index > his_index:
             #New stable match is found for "her"
             woman_spouse[she] = he
             man_spouse[he] = she
             next_man_choice[he] = next_man_choice[he] + 1
             #Pop the newly wed husband
             unmarried_men.pop(0)
             #Now the previous husband is unmarried add
             #him to the unmarried list
             unmarried_men.insert(0,current_husband)
          else:
             next_man_choice[he] = next_man_choice[he] + 1

    return man_spouse, woman_spouse

men_prefereces, women_preferences = simulationMarriageMarket(4, 10, 5, 10)

print(men_prefereces)

print(women_preferences)

men_spouse, women_spouse  = galeShapley(4, 10, men_prefereces, women_preferences)
 

print(men_spouse)

print(women_spouse)

print('code succesfull')