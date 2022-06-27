from statistics import mean
from unittest import skip
import numpy as np
import random as ra
import time

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
        prefs = np.random.choice(schools, n_schools, replace=False)
        student_full_preferences[student] = np.array([(i, prefs[i]) for i in range(n_schools)])
        
    for school in schools: 
        prefs = np.random.choice(students, n_students, replace = False)
        school_full_preferences[school] = np.array([(i, prefs[i]) for i in range(n_students)])

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
    school_possible_partners = {school: np.empty(0) for school in school_full_preferences.keys()}
    
    for student, s_prefs in student_full_preferences.items():
        s_prefs_restricted = s_prefs[np.random.choice(s_prefs.shape[0], d_student, replace=False), :]
        student_preferences[student] = s_prefs_restricted[s_prefs_restricted[:,0].argsort()]
        for school in s_prefs_restricted.T[1, :]:
            school_possible_partners[school] = np.append(school_possible_partners[school], student)
    
    for school, h_prefs in school_full_preferences.items():
        school_preferences[school] = h_prefs[np.in1d(h_prefs[:,1], school_possible_partners[school])]    
    return student_preferences, school_preferences


def increase_preference_sublist(delta, student_preferences, school_preferences, student_full_preferences, school_full_preferences):
    '''
    Function that increases the previously sampled sublist of preferences. 
    Inputs
    '''

    #total_stud_time = 0
    #stud_list_time = 0

    student_preferences_2 = {}
    school_preferences_2 = dict(school_preferences)
    school_possible_partners = {school: pref[:, 1] for school, pref in school_preferences.items()}
    
    for student, prefs in student_preferences.items():
        #start_time = time.time()
        student_full_prefs = student_full_preferences[student]
        student_full_prefs_rows = student_full_prefs.view([('', student_full_prefs.dtype)] * student_full_prefs.shape[1])
        prefs_rows = prefs.view([('', prefs.dtype)] * prefs.shape[1])
        potential_additions = np.setdiff1d(student_full_prefs_rows, prefs_rows).view(student_full_prefs.dtype).reshape(-1, student_full_prefs.shape[1])
        schools_to_add = potential_additions[np.random.choice(potential_additions.shape[0], delta, replace=False), :]
        s_prefs_restricted = np.concatenate((prefs, schools_to_add), axis = 0)
        student_preferences_2[student] = s_prefs_restricted[s_prefs_restricted[:,0].argsort()]
        #stud_list_time += time.time() - start_time
        
        for school in schools_to_add:
            sch = school[1]
            school_possible_partners[sch] = np.append(school_possible_partners[sch], student)
        #total_stud_time += time.time() - start_time
    #Add the student to the preference lists of the schools with a possition with respect to the counselor confidence of placement.
    #start_time = time.time()
    for school, h_prefs in school_full_preferences.items():
        school_preferences_2[school] = h_prefs[np.in1d(h_prefs[:,1], school_possible_partners[school])]
    #school_list_time = time.time() - start_time          
    
    #print("Stud List time --- %s seconds ---" % (stud_list_time))
    #print("School append time --- %s seconds ---" % (total_stud_time))
    #print("School list time --- %s seconds ---" % (school_list_time))    
    return student_preferences_2, school_preferences_2


def gale_shapley_modified(n_students, n_schools, student_preferences, school_preferences):
    '''
    Computes the stable match of a market using the DA algorithm by Gale and Shapley.
    INPUTS:
        n_students: number of students in the market
        n_schools: number of schools in the market
        student_preferences: dictionary with preference lists for students
        school_preferences: dictionary with preference lists for schools
    OUTPUT:
        student_match: list with students stable partner 
        school_match: list with schools stable partner
    '''

    unmatched_students = list(range(n_students))

    student_match = np.full((n_students, 2), -9999, dtype=int)
    school_match = np.full((n_schools, 2), -9999, dtype=int)

    next_student_choice = [0] * n_students

    size_preferences = student_preferences[0].shape[0]

    while unmatched_students: 
        student = unmatched_students[0]
        to_break = 0
        
        while next_student_choice[student]>=size_preferences and to_break == 0:
            if len(unmatched_students)>1:  
                unmatched_students.pop(0)
                student = unmatched_students[0]
            else: 
                to_break = 1
        if to_break == 1: 
            break

        student_pref  = student_preferences[student]
        sch = student_pref[next_student_choice[student]]
        school = sch[1]
        school_pref = school_preferences[school]
        school_current_match = school_match[school]

        if (school_current_match[1] == -9999): 
            school_match[school] = school_pref[school_pref[:,1]==student][0]
            student_match[student] = sch
            next_student_choice[student] = next_student_choice[student] + 1 
            unmatched_students.pop(0)

        else:
            current_index = school_current_match[0]
            stud = school_pref[school_pref[:,1]==student][0]
            candidate_index = stud[0]

            if candidate_index < current_index: 
                school_match[school] = stud
                student_match[student] = sch
                next_student_choice[student] = next_student_choice[student] + 1
                unmatched_students.pop(0)
                unmatched_students.insert(0, school_current_match[1])
                student_match[school_current_match[1]] = [-9999,-9999]

            else:
                next_student_choice[student] = next_student_choice[student] + 1

    return student_match, school_match


def simulation_matching_increase_preferences(Delta, k, n_students, n_schools, additions):
    '''
    Simulates the matching outcome under diferent preference list sizes where we only add new preferences.
    '''
    student_f_pref, school_f_pref = marriage_market_preference_lists(n_students, n_schools)

    student_pre = {}
    school_pre = {}
    student_M = {}
    school_M = {}
    
    student_pre[k], school_pre[k] = restricted_market(k, student_f_pref, school_f_pref)
    student_M[k], school_M[k] = gale_shapley_modified(n_students, n_schools, student_pre[k], school_pre[k])
    
    for j in range(1,additions+1):
        k_prev = k
        k = k + Delta
        print('working on sublist size: ' + str(k))
        student_pre[k], school_pre[k] = increase_preference_sublist(Delta, student_pre[k_prev], school_pre[k_prev], student_f_pref, school_f_pref)
        student_M[k], school_M[k] = gale_shapley_modified(n_students, n_schools, student_pre[k], school_pre[k])
        
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

        for i in range(student_M[k].shape[0]):
            match_prev = student_M[k_prev][i,1]
            match_new = student_M[k][i,1]
            if (match_prev != match_new):
                change.append(1)
            else: 
                change.append(0)
        
        change_match_students[k] = change

        change_school  = []

        for i in range(school_M[k].shape[0]):
            match_new = school_M[k][i, 1]
            match_prev = school_M[k_prev][i, 1]
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
    unmatched_match_students = {}
    unmatched_match_schools = {}

    for j in range(additions):
    
        k_prev = k
        k = k + Delta
        change  = []

        for i in range(student_M[k].shape[0]):
            if (student_M[k][i, 1] != -9999) and (student_M[k_prev][i,1] == -9999): 
                change.append(1)
            else: 
                change.append(0)
        
        unmatched_match_students[k] = change

        change_school  = []

        for i in range(school_M[k].shape[0]):
            if (school_M[k][i,1] != -9999) and (school_M[k_prev][i,1] == -9999):
                change_school.append(1)
            else: 
                change_school.append(0)
        
        unmatched_match_schools[k] = change_school

    return unmatched_match_students, unmatched_match_schools

def total_unmatched_matched(unmatched_match_students, unmatched_match_schools):
    '''
    Computes the total number of students that went from being unmatched
    to being matched while k increases of value
    '''
    num_students_unmatched_matched = {}
    num_schools_unmatched_matched = {}

    for k, changes in unmatched_match_students.items():
        num_students_unmatched_matched[k] = sum(map(lambda x : x == 1, changes))
    
    for k, changes in unmatched_match_schools.items():
        num_schools_unmatched_matched[k] = sum(map(lambda x : x == 1, changes))
    
    return num_students_unmatched_matched, num_schools_unmatched_matched

def change_original_rank(Delta, k , additions, student_M, school_M):
    '''
    Computes how many students obtain an actual better partner
    '''
    change_rank_students = {}
    change_rank_schools = {}

    for j in range(additions):
    
        k_prev = k
        k = k + Delta
        change  = []

        for i in range(student_M[k].shape[0]):
            rank_prev = student_M[k_prev][i,0]
            rank_new = student_M[k][i,0]
            if rank_prev > rank_new:
                change.append(1)
            elif rank_prev < rank_new: 
                change.append(2)
            else: 
                change.append(0)
        
        change_rank_students[k] = change

        change_school  = []

        for i in range(school_M[k].shape[0]):
            rank_prev = school_M[k_prev][i,0]
            rank_new = school_M[k][i,0]
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
    average_num_students_unm_mat = {x : 0 for x in range(beg, end, Delta)}
    average_num_students_imp = {x : 0 for x in range(beg, end, Delta)}
    average_num_schools_change = {x : 0 for x in range(beg, end, Delta)}
    average_num_schools_unm_mat = {x : 0 for x in range(beg, end, Delta)}
    average_num_schools_imp = {x : 0 for x in range(beg, end, Delta)}


    for i in range(iterations):
        print('Working on iteration: ' + str(i))

        student_Match, school_Match, student_original_preferences, school_original_preferences = simulation_matching_increase_preferences(Delta, sublist, n_students, n_schools, additions)

        student_changes, school_changes = differences_match(Delta, sublist, additions, student_Match, school_Match)
        num_students_change, num_schools_change = total_differences_match(student_changes, school_changes)

        unm_mat_students, unm_mat_schools = unmatched_matched(Delta, sublist, additions, student_Match, school_Match)
        num_students_unm_mat, num_schools_unm_mat = total_unmatched_matched(unm_mat_students, unm_mat_schools)

        
        student_changes_orank, school_changes_orank = change_original_rank(Delta, sublist, additions, student_Match, school_Match)
        num_students_imp, num_schools_imp = improve_original_rank(student_changes_orank, school_changes_orank, num_students_change, num_schools_change)

        #Students
        for size, value in num_students_change.items():
            average_num_students_change[size] = average_num_students_change[size] + value/iterations
        
        for size, value in num_students_unm_mat.items():
            average_num_students_unm_mat[size] = average_num_students_unm_mat[size] + value/iterations
        
        for size, value in num_students_imp.items():
            average_num_students_imp[size] = average_num_students_imp[size] + value/iterations
        #Schools
        for size, value in num_schools_change.items():
            average_num_schools_change[size] = average_num_schools_change[size] + value/iterations
        
        for size, value in num_schools_unm_mat.items():
            average_num_schools_unm_mat[size] = average_num_schools_unm_mat[size] + value/iterations
        
        for size, value in num_schools_imp.items():
            average_num_schools_imp[size] = average_num_schools_imp[size] + value/iterations
        
    return average_num_students_change, average_num_schools_change, average_num_students_unm_mat, average_num_schools_unm_mat, average_num_students_imp, average_num_schools_imp
    