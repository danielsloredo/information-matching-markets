from unittest import skip
import numpy as np
import random as ra
import matplotlib.pyplot as plt


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

    for man, prefs in men_preferences.items():
        if men_spouse[man] == None:
            men_ranks[man] = men_rank_unmatched
        else:
            men_ranks[man] = prefs.index(men_spouse[man]) + 1
    
    for woman, prefs in women_preferences.items():
        if women_spouse[woman] == None:
            if women_preferences[woman] != None:
                women_rank_unmatched = len(women_preferences[woman]) + 1
                women_ranks[woman] = women_rank_unmatched
            else:
                skip
        else:
            women_ranks[woman] = prefs.index(women_spouse[woman]) + 1

    men_average_rank = sum(men_ranks.values())/n_men
    women_average_rank = sum(women_ranks.values())/n_women

    return men_average_rank, women_average_rank


def simulationMCMatching(n_men, n_women, men_pref_sizes, women_pref_size, iter):
    '''

    INPUT:

    Output: 
    '''

    rank_size_men = {}
    rank_size_women = {}

    for pref_size in men_pref_sizes:
        print('simulating size of preferences: ' + str(pref_size))
        men_average_ranks = []
        women_average_ranks = []
        for i in range(iter):
            men_pref, women_pref = simulationMarriageMarket(n_men, n_women, pref_size, women_pref_size)
            men_sp, women_sp = galeShapley(n_men, n_women, men_pref, women_pref)
            men_average_r, women_average_r = averageRankPartners(n_men, n_women, men_sp, women_sp, men_pref, women_pref)
            men_average_ranks.append(men_average_r)
            women_average_ranks.append(women_average_r)
        rank_size_men[pref_size] = sum(men_average_ranks)/iter
        rank_size_women[pref_size] = sum(women_average_ranks)/iter
    return rank_size_men, rank_size_women


def counselorIncreasePreferences(n_students, n_preference_additions, students_pref, school_pref, counselor_confidence):
    '''

    INPUT:

    Output: 
    '''
    
    schools = list(school_pref.keys())
    ## Chose students that will hire a counselor
    candidates = np.random.choice(list(students_pref.keys()), n_students, replace = False).tolist()
    #Add the specified amount of schools to the preference list of the student
    schools_to_add = {}
    pos_school_pref = round(10*(1-counselor_confidence))
    for candidate in candidates:
        current_schools = students_pref[candidate]
        potential_additions = list(set(schools).difference(current_schools))
        schools_to_add[candidate] = np.random.choice(potential_additions, n_preference_additions, replace=False).tolist()
        students_pref[candidate] = students_pref[candidate] + schools_to_add[candidate]
        ra.shuffle(students_pref[candidate])
    #Add the student to the preference lists of the schools with a possition with respect to the counselor confidence of placement.
        for school in schools_to_add[candidate]:
            if len(school_pref[school])>pos_school_pref:
                school_pref[school].insert(pos_school_pref, candidate)
            else:
                school_pref[school].append(candidate)
    
    return students_pref, school_pref, candidates

def galeShapleyModified(n_men, n_women, men_preferences, women_preferences):
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
    # While there exists at least one unmarried man or there are men with possible proposals still available:
    while unmarried_men:
        # Pick an arbitrary unmarried man
        he = unmarried_men[0]
        to_break = 0

        while next_man_choice[he]>=len(men_preferences[he]) and to_break==0:
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


def averageRankPartnersModified(student_spouse, school_spouse, student_preferences, school_preferences, modified_candidates):
    '''

    INPUT:

    Output: 
    '''
    student_ranks = {}
    school_ranks = {}

    for student, prefs in student_preferences.items():
        if student_spouse[student] == None:
            student_rank_unmatched = len(student_preferences[student]) + 1
            student_ranks[student] = student_rank_unmatched
        else:
            student_ranks[student] = prefs.index(student_spouse[student]) + 1
    
    for school, prefs in school_preferences.items():
        if school_spouse[school] == None:
            if school_preferences[school] != None:
                school_rank_unmatched = len(school_preferences[school]) + 1
                school_ranks[school] = school_rank_unmatched
            else:
                skip
        else:
            school_ranks[school] = prefs.index(school_spouse[school]) + 1

    noncandidates = list(set(student_preferences.keys()).difference(modified_candidates)) 
    candidate_ranks = {cand: student_ranks[cand] for cand in modified_candidates}
    candidates_average_rank = sum(candidate_ranks.values())/len(modified_candidates)    
    noncandidate_ranks = {cand: student_ranks[cand] for cand in noncandidates}
    noncandidates_average_rank = sum(noncandidate_ranks.values())/len(noncandidates)

    school_average_rank = sum(school_ranks.values())/len(list(school_preferences.keys()))

    return school_average_rank, candidates_average_rank, noncandidates_average_rank

def simulationPreferenceAdditions(n_students, n_schools, student_pref_sizes, school_pref_size, students_to_modify, schools_to_add, counselor_confidence, iter):
    '''

    INPUT:

    Output: 
    '''

    rank_candidates = {}
    rank_school = {}
    rank_noncandidates = {}

    for extra_schools in schools_to_add:
        print('simulating with addittion to preferences of : ' + str(extra_schools))
        candidate_average_ranks = []
        school_average_ranks = []
        noncandidates_average_ranks = []

        for i in range(iter):
            if i % 10 == 0:
                print('working on iteration: ' + str(i))

            student_pref, school_pref = simulationMarriageMarket(n_students, n_schools, student_pref_sizes, school_pref_size)
            student_pref_2, school_pref_2, candidates = counselorIncreasePreferences(students_to_modify, extra_schools, student_pref, school_pref, counselor_confidence)
            student_sp, school_sp = galeShapleyModified(n_students, n_schools, student_pref_2, school_pref_2)
            
            school_average_r, candidate_av_rank, noncandidates_av_rank = averageRankPartnersModified(student_sp, school_sp, student_pref_2, school_pref_2, candidates)
            candidate_average_ranks.append(candidate_av_rank)
            school_average_ranks.append(school_average_r)
            noncandidates_average_ranks.append(noncandidates_av_rank)
            
        rank_school[extra_schools] = sum(school_average_ranks)/iter
        rank_candidates[extra_schools] = sum(candidate_average_ranks)/iter
        rank_noncandidates[extra_schools] = sum(noncandidates_average_ranks)/iter

    return rank_school, rank_candidates, rank_noncandidates
