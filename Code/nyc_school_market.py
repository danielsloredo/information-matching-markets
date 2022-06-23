from statistics import mean
from unittest import skip
import numpy as np
import random as ra

def marriage_market_preference_lists(n_students, n_schools):
    '''
    Function that generates a random bipartite matching market instance between students and 
    schools with complete preference lists on the opposite side
    Inputs: 
        -n_students: number of students in the market
        -n_schools: number of schools in the market
    Outputs: 
        -student_full_preferences: dictionary with list of preferences for each one of the students
        -school_full_preferences: dictionary with list of preferences for each one of the schools
    '''

    students = [i for i in range(n_students)]
    schools = [i for i in range(n_schools)]

    student_full_preferences = {}
    school_full_preferences = {}

    for student in students: 
        student_full_preferences[student] = np.random.choice(schools, n_schools, replace=False).tolist()
    for school in schools: 
        school_full_preferences[school] = np.random.choice(students, n_students, replace = False).tolist()

    return student_full_preferences, school_full_preferences

def restricted_market(d_student, student_full_preferences, school_full_preferences):
    '''
    Function that samples a sublist of preferences from the full preference lists of agents in the 
    random matching market.
    Inputs: 
        -d_student: lenght of preferences on students sub-list
        -student_full_preferences: Dictionary with list of preferences for each one of the students in the market
        -school_full_preferences: Dictionary with list of preferences for each one of the schools in the market
    Output: 
        -student_preferences: dictionary with preference sublists for students in the market
        -school_preferences: dictionary with preference sublists for schools in the market
    '''

    student_preferences = {}
    school_preferences = {}

    for student, s_prefs in student_full_preferences.items():
        student_preferences[student] = [s_prefs[i] for i in sorted(ra.sample(range(len(s_prefs)), d_student))]

    for school, h_prefs in school_full_preferences.items():
        possible_partners = []
        for student, prefs in student_preferences.items():
            if school in prefs:
                possible_partners.append(student)
        number_poss_partners = len(possible_partners)
        if number_poss_partners > 0:
            school_preferences[school] = [std for std in school_full_preferences[school] if std in possible_partners]
        else:
            school_preferences[school] = None
    
    return student_preferences, school_preferences

def increase_preference_sublist(delta, student_preferences, school_preferences, student_full_preferences, school_full_preferences):
    '''
    Function that increases the previously sampled sublist of preferences. 
    Inputs
    '''
    student_preferences_2 = {}
    school_preferences_2 = dict(school_preferences)
    schools = list(school_preferences.keys())
    for student, prefs in student_preferences.items():
        current_schools = prefs
        potential_additions = list(set(schools).difference(current_schools))
        schools_to_add = ra.sample(potential_additions, delta)
        new_list = student_preferences[student] + schools_to_add
        student_preferences_2[student] = [sch for sch in student_full_preferences[student] if sch in new_list]
    #Add the student to the preference lists of the schools with a possition with respect to the counselor confidence of placement.
        for school in schools_to_add:
            if school_preferences_2[school]==None:
                school_preferences_2[school]=[student]
            else:
                new_list_s=school_preferences_2[school] + [student]
                school_preferences_2[school] = [std for std in school_full_preferences[school] if std in new_list_s]
    
    return student_preferences_2, school_preferences_2


def gale_shapley_modified(n_men, n_women, men_preferences, women_preferences):
    '''
    Computes the stable match of a market using the DA algorithm by Gale and Shapley.
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

    size_preferences = len(men_preferences[0])                    
    # While there exists at least one unmarried man or there are men with possible proposals still available:
    while unmarried_men:
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
             man_spouse[current_husband] = None

          else:
             next_man_choice[he] = next_man_choice[he] + 1

    return man_spouse, woman_spouse

def rank_partners(student_spouse, school_spouse, student_preferences, school_preferences):
    '''
    Computes the rank of the partner of the agents on the stable match outcome
    '''    
    student_ranks = [None]*len(student_preferences.keys())
    school_ranks = [None]*len(school_preferences.keys())

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
                school_ranks[school] = None
        else:
            school_ranks[school] = prefs.index(school_spouse[school]) + 1

    return student_ranks, school_ranks

def average_rank_partners(student_spouse, school_spouse, student_preferences, school_preferences):
    '''
    Computes the average rank of partner for the agents on the stable outcome
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

    student_average_rank = sum(student_ranks.values())/len(list(student_ranks.keys()))
    school_average_rank = sum(school_ranks.values())/len(list(school_ranks.keys()))

    return student_average_rank, school_average_rank

def simulation_matching_market(n_students, n_schools, preferences_size, iterations):
    '''
    Simulates a random matching market with different sizes of preferences
    '''

    student_f_pref, school_f_pref = marriage_market_preference_lists(n_students, n_schools)

    student_average_rank = {}
    school_average_rank = {}
    student_rank = {list_size: [] for list_size in preferences_size}
    school_rank = {list_size: [] for list_size in preferences_size}

    for i in range(iterations):
        print('working on iteration: ' + str(i))

        student_pre = {}
        school_pre = {}
        student_sp = {}
        school_sp = {}

        for list_size in preferences_size:
            print('simulating with students preference list size: ' + str(list_size))

            student_pre[list_size], school_pre[list_size] = restricted_market(list_size, student_f_pref, school_f_pref)
            student_sp[list_size], school_sp[list_size] = gale_shapley_modified(n_students, n_schools, student_pre[list_size], school_pre[list_size])
            student_r, school_r = average_rank_partners(student_sp[list_size], school_sp[list_size], student_pre[list_size], school_pre[list_size])
            student_rank[list_size].append(student_r)
            school_rank[list_size].append(school_r) 
        student_average_rank[list_size] = 1/iterations * sum(student_rank[list_size])
        school_average_rank[list_size] = 1/iterations * sum(school_rank[list_size])

    return student_f_pref, student_average_rank, school_f_pref, school_average_rank
    
def simulation_matching_increase_preferences(Delta, k, n_students, n_schools, additions):
    '''
    Simulates the matching outcome under diferent preference list sizes where we only add new preferences.
    '''
    student_f_pref, school_f_pref = marriage_market_preference_lists(n_students, n_schools)

    student_pre = {}
    school_pre = {}
    student_M = {}
    school_M = {}
    #student_M_rank = {}
    #school_M_rank = {}
    
    student_pre[k], school_pre[k] = restricted_market(k, student_f_pref, school_f_pref)
    student_M[k], school_M[k] = gale_shapley_modified(n_students, n_schools, student_pre[k], school_pre[k])
    #student_M_rank[k], school_M_rank[k] = rank_partners(student_M[k], school_M[k], student_pre[k], school_pre[k])
    
    for j in range(1,additions+1):
        k_prev = k
        k = k + Delta
        print('working on sublist size: ' + str(k))
        student_pre[k], school_pre[k] = increase_preference_sublist(Delta, student_pre[k_prev], school_pre[k_prev], student_f_pref, school_f_pref)
        student_M[k], school_M[k] = gale_shapley_modified(n_students, n_schools, student_pre[k], school_pre[k])
        #student_M_rank[k], school_M_rank[k] = rank_partners(student_M[k], school_M[k], student_pre[k], school_pre[k])

    return student_M, school_M, student_f_pref, school_f_pref

def differences_match(Delta, k , additions, student_M, school_M):
    '''
    Computes the change in stable outcome
    '''
    change_match_students = {}
    change_match_schools = {}

    for j in range(additions):
    
        k_prev = k
        k = k + Delta
        change  = []

        for i in range(len(student_M[k])):
            match_prev = student_M[k_prev][i]
            match_new = student_M[k][i]
            if (match_prev != match_new):
                change.append(1)
            else: 
                change.append(0)
        
        change_match_students[k] = change

        change_school  = []

        for i in range(len(school_M[k])):
            match_new = school_M[k][i]
            match_prev = school_M[k_prev][i]
            if (match_prev != match_new):
                change_school.append(1)
            else: 
                change_school.append(0)
        
        change_match_schools[k] = change_school

    return change_match_students, change_match_schools


def total_differences_match(change_match_students, change_match_schools):
    '''
    Computes total change on the stable outcomes
    '''
    num_students_change = {}
    num_schools_change = {}

    for k, changes in change_match_students.items():
        num_students_change[k] = sum(map(lambda x : x == 1, changes))
    
    for k, changes in change_match_schools.items():
        num_schools_change[k] = sum(map(lambda x : x == 1, changes))
    
    return num_students_change, num_schools_change

def unmatched_matched(Delta, k , additions, student_M, school_M):
    '''
    Function that tells us how many students went from being unmatched to being match when k increases
    '''
    change_match_students = {}
    change_match_schools = {}

    for j in range(additions):
    
        k_prev = k
        k = k + Delta
        change  = []

        for i in range(len(student_M[k])):
            if (student_M[k][i] != None) and (student_M[k_prev][i] == None): 
                change.append(1)
            else: 
                change.append(0)
        
        change_match_students[k] = change

        change_school  = []

        for i in range(len(school_M[k])):
            if (school_M[k][i] != None) and (school_M[k_prev][i] == None):
                change_school.append(1)
            else: 
                change_school.append(0)
        
        change_match_schools[k] = change_school

    return change_match_students, change_match_schools

def total_unmatched_matched(change_match_students, change_match_schools):
    '''
    Computes the total number of students that went from being unmatched
    to being matched while k increases of value
    '''
    num_students_change = {}
    num_schools_change = {}

    for k, changes in change_match_students.items():
        num_students_change[k] = sum(map(lambda x : x == 1, changes))
    
    for k, changes in change_match_schools.items():
        num_schools_change[k] = sum(map(lambda x : x == 1, changes))
    
    return num_students_change, num_schools_change

def original_rank(student_M, school_M, student_original_pref, school_original_pref):
    '''
    Computes the rank of partner according to the full list of preferences for each agent
    '''

    student_ranks = {k: [None]*len(s) for k, s in student_M.items()}
    school_ranks = {k: [None]*len(s) for k, s in school_M.items()}

    for k, spouses in student_M.items():
        for student, prefs in student_original_pref.items():
            if spouses[student] == None:
                student_rank_unmatched = len(prefs) + 1
                student_ranks[k][student] = student_rank_unmatched
            else: 
                student_ranks[k][student] = prefs.index(spouses[student]) + 1
    
    for k, spouses in school_M.items():
        for school, prefs in school_original_pref.items():
            if spouses[school] == None:
                if prefs != None:
                    school_rank_unmatched = len(prefs) + 1
                    school_ranks[k][school] = school_rank_unmatched
                else:
                    school_ranks[k][school] = None
            else:
                school_ranks[k][school] = prefs.index(spouses[school]) + 1   
                
    return student_ranks, school_ranks

def change_original_rank(Delta, k , additions, student_ranks, school_ranks):
    '''
    Computes how many students obtain an actual better partner
    '''
    change_rank_students = {}
    change_rank_schools = {}

    for j in range(additions):
    
        k_prev = k
        k = k + Delta
        change  = []

        for i in range(len(student_ranks[k])):
            rank_prev = student_ranks[k_prev][i]
            rank_new = student_ranks[k][i]
            if rank_prev > rank_new:
                change.append(1)
            elif rank_prev < rank_new: 
                change.append(2)
            else: 
                change.append(0)
        
        change_rank_students[k] = change

        change_school  = []

        for i in range(len(school_ranks[k])):
            rank_prev = school_ranks[k_prev][i]
            rank_new = school_ranks[k][i]
            if rank_prev > rank_new:
                change_school.append(1)
            elif rank_prev < rank_new: 
                change_school.append(2)
            else: 
                change_school.append(0)
        
        change_rank_schools[k] = change_school

    return change_rank_students, change_rank_schools


def improve_original_rank(change_rank_students, change_rank_schools, num_students_change, num_schools_change):
    '''
    Gives the percentage of students that improved partner on the original list when changing partner 
    between sublist sizes
    '''
    pct_students_improve = {}
    pct_schools_improve = {}

    for k, changes in change_rank_students.items():
        if num_students_change[k] > 0: 
            pct_students_improve[k] = sum(map(lambda x : x == 1, changes))/num_students_change[k]
        else: 
            pct_students_improve[k] = 0
    
    for k, changes in change_rank_schools.items():
        if num_schools_change[k] > 0: 
            pct_schools_improve[k] = sum(map(lambda x : x == 1, changes))/num_schools_change[k]
        else: 
            pct_schools_improve[k] = 0

    return pct_students_improve, pct_schools_improve


def mc_simulations_improvement(Delta, sublist, additions, n_students, n_schools, iterations):
    '''
    Monte Carlo simulations of the percentage of students that improved partner between stable outcomes
    '''
    
    beg = sublist + Delta
    end = sublist+Delta*additions + Delta
    average_num_students_change = {x : 0 for x in range(beg, end, Delta)}
    average_num_students_imp = {x : 0 for x in range(beg, end, Delta)}


    for i in range(iterations):
        print('Working on iteration: ' + str(i))

        student_Match, school_Match, student_original_preferences, school_original_preferences = simulation_matching_increase_preferences(Delta, sublist, n_students, n_schools, additions)

        student_changes, school_changes = differences_match(Delta, sublist, additions, student_Match, school_Match)
        num_students_change, num_schools_change = total_differences_match(student_changes, school_changes)

        student_original_ranks, school_original_ranks = original_rank(student_Match, school_Match, student_original_preferences, school_original_preferences)    
        student_changes_orank, school_changes_orank = change_original_rank(Delta, sublist, additions, student_original_ranks, school_original_ranks)
        num_students_imp, num_schools_imp = improve_original_rank(student_changes_orank, school_changes_orank, num_students_change, num_schools_change)

        for size, value in num_students_change.items():
            average_num_students_change[size] = average_num_students_change[size] + value/iterations
        
        for size, value in num_students_imp.items():
            average_num_students_imp[size] = average_num_students_imp[size] + value/iterations
        
        
    return average_num_students_change, average_num_students_imp

