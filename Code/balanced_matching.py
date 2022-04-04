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
        possible_partners = []
        for man, prefs in men_preferences.items():
            if woman in prefs:
                possible_partners.append(man)
        number_poss_partners = len(possible_partners)
        if number_poss_partners > 0:
            if number_poss_partners < d_women:
                women_preferences[woman] = np.random.choice(possible_partners, number_poss_partners, replace=False).tolist()
            else:
                women_preferences[woman] = np.random.choice(possible_partners, d_women, replace=False).tolist()
        else:
            women_preferences[woman] = None
    
    return men_preferences, women_preferences

def galeShapley(n_men, n_women, men_preferences, women_preferences):
    '''
    Function that computes the stable match of a market using the DA algorithm by Gale and Shapley.
    INPUTS:
        n_men: number of men in the market
        n_women: number of women in the market
        men_preferences: dictionary with preference lists for men
        women_preferences: dictionary with preference lists for women
    OUTPUT:
        man_spouse: list with men stable partner 
        woman_spouse: list with women stable partner
    '''
    # Initially, all n men are unmarried
    unmarried_men = list(range(n_men))
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
    while unmarried_men and (sum(next_man_choice) <= total_posible_proposals):
        # Pick an arbitrary unmarried man
        he = unmarried_men[0]
        to_break = 0

        while next_man_choice[he]>=size_preferences and to_break==0:
            if len(unmarried_men)>1:
                unmarried_men.pop(0)
                he = unmarried_men[0]
            else:
                to_break = 1

        if to_break == 1:
            break

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

def averageRankPartners(n_men, n_women, men_spouse, women_spouse, men_preferences, women_preferences):
    '''
    Function that computes the average rank of partners in the stable match
    INPUT:
        n_men: number of men in the market
        n_women: number of women in the market
        men_spouse: list with stable partners for men
        women_spouse: list with stable partners for women
        men_preferences: dictionary with the list of preferences for each one of the men
        women_preferences: dictionary with the list of preferences for each one of the women
    Output: 
        men_average_rank: average rank of partners for men in the stable match
        women_average_rank: average rank of partners for women in the stable match
    '''
    men_ranks = {}
    women_ranks = {}
    men_rank_unmatched = len(men_preferences[0]) + 1
    women_rank_unmatched = len(women_preferences[0]) + 1

    for man, prefs in men_preferences.items():
        if men_spouse[man] == None:
            men_ranks[man] = men_rank_unmatched
        else:
            men_ranks[man] = prefs.index(men_spouse[man]) + 1
    
    for woman, prefs in women_preferences.items():
        if women_spouse[woman] == None:
            women_ranks[woman] = women_rank_unmatched
        else:
            women_ranks[woman] = prefs.index(women_spouse[woman]) + 1

    men_average_rank = sum(men_ranks.values())/n_men
    women_average_rank = sum(women_ranks.values())/n_women

    return men_average_rank, women_average_rank


men_preferences, women_preferences = simulationMarriageMarket(1000, 1001, 150, 1000)

men_spouse, women_spouse  = galeShapley(1000, 1001, men_preferences, women_preferences)

men_average_rank, women_average_rank = averageRankPartners(1000, 1001, men_spouse, women_spouse, men_preferences, women_preferences)

print(men_average_rank)

print(women_average_rank)

print('code succesfull')