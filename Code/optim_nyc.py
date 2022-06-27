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