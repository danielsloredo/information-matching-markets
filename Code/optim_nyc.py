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
        
        while next_student_choice[student]>=student_preferences[student].shape[0] and to_break == 0:
            if len(unmatched_students)>1:  
                unmatched_students.pop(0)
                student = unmatched_students[0]
            else: 
                to_break = 1
        if to_break == 1: 
            break

        student_pref  = np.copy(student_preferences[student])
        sch = np.copy(student_pref[next_student_choice[student]])
        school = sch[1]
        school_pref = np.copy(school_preferences[school])
        school_current_match = np.copy(school_match[school])
        
        if (school_current_match[1] == -9999): 
            stud = np.copy(school_pref[school_pref[:,1]==student][0])
            school_match[school] = stud
            student_match[student] = sch
            next_student_choice[student] = next_student_choice[student] + 1 
            unmatched_students.pop(0)
        
        else:
            current_index = school_current_match[0]
            stud = np.copy(school_pref[school_pref[:,1]==student][0])
            candidate_index = stud[0]
        
            if candidate_index < current_index: 
                student_match[school_current_match[1]] = [-9999,-9999]
                school_match[school] = stud
                student_match[student] = sch
                next_student_choice[student] = next_student_choice[student] + 1
                unmatched_students.pop(0)
                unmatched_students.insert(0, school_current_match[1])
        
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
            if (match_prev != match_new) and (match_new != -9999):
                change.append(1)
            else: 
                change.append(0)
        
        change_match_students[k] = change

        change_school  = []

        for i in range(school_M[k].shape[0]):
            match_new = school_M[k][i, 1]
            match_prev = school_M[k_prev][i, 1]
            if (match_prev != match_new) and (match_new != -9999):
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

def nash_welfare(student_M, school_M): 
    
    nash_welfare_students = {}

    for size, match in student_M.items():
        ranks = np.copy(match[:, 0])
        utility = np.array(school_M[size].shape[0]+2-ranks[ranks!=-9999], dtype=float)
        nash_welfare_students[size] = np.power(utility.prod(),(1/match.shape[0]))
    
    nash_welfare_schools = {}

    for size, match in school_M.items():
        ranks = match[:, 0]
        utility = np.array(student_M[size].shape[0]+2-ranks[ranks!=-9999], dtype=float)
        nash_welfare_schools[size] = np.power(utility.prod(),(1/match.shape[0]))

    return nash_welfare_students, nash_welfare_schools

def average_rank_match(student_M, school_M):

    oranks_students = {} 
    oranks_schools = {}

    average_oranks_students = {} 
    average_oranks_schools = {}


    for size, match in student_M.items():
        ranks = np.copy(match[:,0])
        ranks[ranks == -9999] =  school_M[size].shape[0]
        ranks[:] += 1
        oranks_students[size] = ranks.tolist()
        average_oranks_students[size] = np.mean(ranks)
    
    for size, match in school_M.items():
        ranks = np.copy(match[:,0])
        ranks[ranks == -9999] =  student_M[size].shape[0]
        ranks[:] += 1
        oranks_schools[size] = ranks.tolist()
        average_oranks_schools[size] = np.mean(ranks)

    return average_oranks_students, average_oranks_schools, oranks_students, oranks_schools

def rank_profile(student_M, school_M): 
    
    ranks_profile = {}

    for size, match in student_M.items(): 
        n_schools = school_M[size].shape[0]
        r_profile =[0 for i in range(n_schools+1)]
        ranks = np.copy(match[:,0])
        ranks[ranks == -9999] = n_schools
        ranks[:] += 1
        ranks_list = ranks.tolist()
        for rk in ranks_list:
            r_profile[rk-1] += 1
        
        ranks_profile[size] = np.array(r_profile)

    return ranks_profile

def utility_functions(student_M, school_M, ranks_p): 
    
    leontief_utility = {}
    miscelaneous_3_utility = {}
    exponential_utility = {}
    s_shape_utility = {}

    for size, match in student_M.items():
        ranks = np.copy(match[:,0])
        ranks[ranks == -9999] =  school_M[size].shape[0]
        ranks[:] += 1
        ranks_float = ranks.astype(np.float64)
        utility = np.reciprocal(ranks_float)
        leontief_utility[size] = np.min(utility)

        coefs = school_M[size].shape[0] + 2 - ranks_float
        utility_misc = 1/2 - np.reciprocal(np.power(coefs, 2))/2
        miscelaneous_3_utility[size] = utility_misc.sum()

        exps = school_M[size].shape[0] + 1 - ranks_float
        utility_exp = 1 - np.exp(-1 * exps)
        exponential_utility[size] = utility_exp.sum()   

        mid_point = school_M[size].shape[0] // 2
        ranks_half_1 = ranks_float[:mid_point]
        ranks_half_2 = ranks_float[mid_point:]
        exps_1 = school_M[size].shape[0] + 1 - ranks_half_1 - mid_point
        exps_2 = school_M[size].shape[0] + 1 - ranks_half_2 - mid_point
        utility_shape_1 = 1 - np.exp(-1 * exps)
        utility_shape_2 = (1 - np.exp(exps)) * (-2)
        s_shape_utility[size] = utility_shape_1.sum() + utility_shape_2.sum()
        
    
    cobb_stone_utility = {}
    qlinear_power_utility = {}
    qlinear_square_utility = {}
    miscelaneous_1_utility = {}
    miscelaneous_2_utility = {}

    random_key = ra.choice(list(ranks_p))
    n_ranks = ranks_p[random_key].shape[0]
    ranks_match = range(n_ranks)
    exponents = [(n_ranks + 1 - i)/n_ranks for i in ranks_match]
    coefficients = [n_ranks + 1 - i for i in ranks_match]
    #ranks_match_array = np.array(ranks_match)
    exponents_array = np.array(exponents)
    coefficients_array = np.array(coefficients)


    for size, prfl in ranks_p.items():
        profile = prfl.astype(np.float64)
        profile_1 = np.copy(profile) + 1
        utility_1 = np.power(profile_1, exponents_array)
        cobb_stone_utility[size] = utility_1.prod()

        profile_unmatched = profile[-1:].item()

        utility_2 = np.power(profile[:-1], exponents_array[:-1])
        utility_3 = np.power(profile[:-1], 2)
        qlinear_power_utility[size] = utility_2.sum() - profile_unmatched
        qlinear_square_utility[size] = utility_3.sum() - profile_unmatched

        utility_4 = utility_1[:-1]
        utility_4_1 = utility_1[1:]
        miscelaneous_1_utility[size] = utility_4.prod()/utility_4_1.prod()

        iso_term = np.power(np.multiply(profile_1, coefficients_array), 2)
        utility_5 = (1 - np.reciprocal(iso_term, where= iso_term!=0)) /2
        miscelaneous_2_utility[size] = utility_5.sum()

    return (leontief_utility, cobb_stone_utility, qlinear_power_utility, qlinear_square_utility, 
    miscelaneous_1_utility, miscelaneous_2_utility, miscelaneous_3_utility,
    exponential_utility, s_shape_utility)


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
    average_nash_welfare_students = {x : 0 for x in range(sublist, end, Delta)}
    average_nash_welfare_schools = {x : 0 for x in range(sublist, end, Delta)}

    average_oranks_students = {x : 0 for x in range(sublist, end, Delta)}
    average_oranks_schools = {x : 0 for x in range(sublist, end, Delta)}
    ranks_students = {x : [] for x in range(sublist, end, Delta)}
    ranks_schools = {x : [] for x in range(sublist, end, Delta)}


    for i in range(iterations):
        print('Working on iteration: ' + str(i))

        student_Match, school_Match, student_original_preferences, school_original_preferences = simulation_matching_increase_preferences(Delta, sublist, n_students, n_schools, additions)

        student_changes, school_changes = differences_match(Delta, sublist, additions, student_Match, school_Match)
        num_students_change, num_schools_change = total_differences_match(student_changes, school_changes)

        unm_mat_students, unm_mat_schools = unmatched_matched(Delta, sublist, additions, student_Match, school_Match)
        num_students_unm_mat, num_schools_unm_mat = total_unmatched_matched(unm_mat_students, unm_mat_schools)

        
        student_changes_orank, school_changes_orank = change_original_rank(Delta, sublist, additions, student_Match, school_Match)
        num_students_imp, num_schools_imp = improve_original_rank(student_changes_orank, school_changes_orank, num_students_change, num_schools_change)

        nash_welfare_students, nash_welfare_schools = nash_welfare(student_Match, school_Match)
        mean_original_ranks_students, mean_original_ranks_schools, or_students, or_schools = average_rank_match(student_Match, school_Match)

        #Students
        for size, value in num_students_change.items():
            average_num_students_change[size] += value/iterations
        
        for size, value in num_students_unm_mat.items():
            average_num_students_unm_mat[size] += value/iterations
        
        for size, value in num_students_imp.items():
            average_num_students_imp[size] += value/iterations

        for size, value in nash_welfare_students.items():
            average_nash_welfare_students[size] += value/iterations

        for size, value in mean_original_ranks_students.items():
            average_oranks_students[size] += value/iterations 

        for size, ary in or_students.items():
            ranks_students[size].extend(ary)

        #Schools
        for size, value in num_schools_change.items():
            average_num_schools_change[size] += value/iterations
        
        for size, value in num_schools_unm_mat.items():
            average_num_schools_unm_mat[size] += value/iterations
        
        for size, value in num_schools_imp.items():
            average_num_schools_imp[size] += value/iterations

        for size, value in nash_welfare_schools.items():
            average_nash_welfare_schools[size] += value/iterations

        for size, value in mean_original_ranks_schools.items():
            average_oranks_schools[size] += value/iterations

        for size, ary in or_schools.items():
            ranks_schools[size].extend(ary)
        
        
    return (average_num_students_change, average_num_schools_change, average_num_students_unm_mat, 
    average_num_schools_unm_mat, average_num_students_imp, average_num_schools_imp, 
    average_nash_welfare_students, average_nash_welfare_schools, average_oranks_students, average_oranks_schools,
    ranks_students, ranks_schools)


def mc_simulations_utility(Delta, sublist, additions, n_students, n_schools, iterations):
    '''
    Function to simulate the behaviour of different utility functions on the stable match
    outcome with different sublist sizes.
    '''
    beg = sublist + Delta
    end = sublist+Delta*additions + Delta
    
    average_nash_welfare_students = {x : 0 for x in range(sublist, end, Delta)}
    average_nash_welfare_schools = {x : 0 for x in range(sublist, end, Delta)}

    average_leontief_utility = {x : 0 for x in range(sublist, end, Delta)} 
    average_cobb_stone_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_qlinear_power_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_qlinear_square_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_miscelaneous_1_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_miscelaneous_2_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_miscelaneous_3_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_exponential_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_s_shape_utility = {x : 0 for x in range(sublist, end, Delta)}
    

    average_oranks_students = {x : 0 for x in range(sublist, end, Delta)}
    average_oranks_schools = {x : 0 for x in range(sublist, end, Delta)}
    ranks_students = {x : [] for x in range(sublist, end, Delta)}
    ranks_schools = {x : [] for x in range(sublist, end, Delta)}
    r_profile = {x : np.zeros(n_schools+1) for x in range(sublist, end, Delta)}


    for i in range(iterations):
        print('Working on iteration: ' + str(i))

        student_Match, school_Match, student_original_preferences, school_original_preferences = simulation_matching_increase_preferences(Delta, sublist, n_students, n_schools, additions)

        nash_welfare_students, nash_welfare_schools = nash_welfare(student_Match, school_Match)
        mean_original_ranks_students, mean_original_ranks_schools, or_students, or_schools = average_rank_match(student_Match, school_Match)
        ranks_profile = rank_profile(student_Match, school_Match)
        (leontief_u, cobb_stone_u, qlinear_power_u, qlinear_square_u, 
        miscelaneous_1_u, miscelaneous_2_u, miscelaneous_3_u,
        exponential_u, s_shape_u) = utility_functions(student_Match, school_Match, ranks_profile)


        #Students
        for size, value in nash_welfare_students.items():
            average_nash_welfare_students[size] += value/iterations

        for size, value in mean_original_ranks_students.items():
            average_oranks_students[size] += value/iterations 

        for size, ary in or_students.items():
            ranks_students[size].extend(ary)
        
        for size, rk_profile in ranks_profile.items():
            r_profile[size] = r_profile[size] + rk_profile/iterations  
        
        for size, value in leontief_u.items():
            average_leontief_utility[size] += value/iterations

        for size, value in cobb_stone_u.items():
            average_cobb_stone_utility[size] += value/iterations

        for size, value in qlinear_power_u.items():
            average_qlinear_power_utility[size] += value/iterations

        for size, value in qlinear_square_u.items():
            average_qlinear_square_utility[size] += value/iterations

        for size, value in miscelaneous_1_u.items():
            average_miscelaneous_1_utility[size] += value/iterations
        
        for size, value in miscelaneous_2_u.items():
            average_miscelaneous_2_utility[size] += value/iterations

        for size, value in miscelaneous_3_u.items():
            average_miscelaneous_3_utility[size] += value/iterations
        
        for size, value in exponential_u.items():
            average_exponential_utility[size] += value/iterations

        for size, value in s_shape_u.items():
            average_s_shape_utility[size] += value/iterations 

        #Schools

        for size, value in nash_welfare_schools.items():
            average_nash_welfare_schools[size] += value/iterations

        for size, value in mean_original_ranks_schools.items():
            average_oranks_schools[size] += value/iterations

        for size, ary in or_schools.items():
            ranks_schools[size].extend(ary)

    return (average_nash_welfare_students, average_nash_welfare_schools, 
    average_oranks_students, average_oranks_schools,
    ranks_students, ranks_schools, 
    r_profile, 
    average_leontief_utility, average_cobb_stone_utility, 
    average_qlinear_power_utility, average_qlinear_square_utility, 
    average_miscelaneous_1_utility, average_miscelaneous_2_utility,
    average_miscelaneous_3_utility, average_exponential_utility,
    average_s_shape_utility) 

def expected_number_students(ranks_profile, n_schools):
    e_n_students_k = {x+1 : [] for x in range(n_schools+1)}
    for size, profile in ranks_profile.items():
        for i in range(len(profile)):
            temp_profile = profile[:i+1]
            e_n_students_k[i+1].append(temp_profile.sum()) 
    return e_n_students_k


def expected_value(values, weights):
    values = np.asarray(values)
    return (values * weights).sum() / weights.sum()

def expected_rank_partner(ranks_profile, n_schools):
    e_rank_k = {x+1 : [] for x in range(n_schools+1)}
    for size, profile in ranks_profile.items():
        for i in range(len(profile)):
            ranks = [j for j in range(i+1)]
            temp_profile = profile[:i+1]
            i_items_sum = temp_profile.sum()
            weights_temp_profile = temp_profile/i_items_sum
            e_rank_k[i+1].append(expected_value(ranks, weights_temp_profile))
    return e_rank_k 



###########
#Functions to check for bad edges
###########
def change_original_rank_bad_edge(student_Match, student_M):
    '''
    Computes how many students obtain an actual better partner
    '''
    change  = []
    bad_edge = False

    for i in range(student_Match.shape[0]):
        rank_prev = student_Match[i,0]
        rank_new = student_M[i,0]
        if rank_prev == -9999 and rank_new == -9999:
            change.append(0) 
        elif rank_prev == -9999 and rank_new != -9999:
            change.append(1)
        elif rank_prev > rank_new:
            change.append(1)
        elif rank_prev < rank_new: 
            change.append(2)
        else: 
            change.append(0)

    if 2 in change:
        if 1 not in change: 
            bad_edge = True

    return bad_edge


def search_bad_edge(student_preferences, school_preferences, student_full_preferences, school_full_preferences, student_Match):
    ''' 
    Inputs
    '''

    n_students = len(student_preferences.keys())
    n_schools = len(school_preferences.keys())

    student_preferences_2 = dict(student_preferences)
    school_preferences_2 = dict(school_preferences)
    school_possible_partners = {school: pref[:, 1] for school, pref in school_preferences.items()}

    bad_e = False
    
    for student, prefs in student_preferences.items():

        if bad_e == False:
            student_full_prefs = student_full_preferences[student]
            student_full_prefs_rows = student_full_prefs.view([('', student_full_prefs.dtype)] * student_full_prefs.shape[1])
            prefs_rows = prefs.view([('', prefs.dtype)] * prefs.shape[1])
            potential_additions = np.setdiff1d(student_full_prefs_rows, prefs_rows).view(student_full_prefs.dtype).reshape(-1, student_full_prefs.shape[1])
            for new_edge in potential_additions:
                if bad_e == False:
                    s_prefs_restricted = np.vstack((prefs, new_edge))
                    student_preferences_2[student] = s_prefs_restricted[s_prefs_restricted[:,0].argsort()]

                    sch = new_edge[1]
                    school_possible_partners[sch] = np.append(school_possible_partners[sch], student)
                    h_prefs = school_full_preferences[sch]
                    school_preferences_2[sch] = h_prefs[np.in1d(h_prefs[:,1], school_possible_partners[sch])]

                    student_M, school_M = gale_shapley_modified(n_students, n_schools, student_preferences_2, school_preferences_2)

                    ## Measure change on stable match

                    bad_e = change_original_rank_bad_edge(student_Match, student_M)
                else: 
                    break
        else: 
            break

    return bad_e



def bad_edges(Delta, k, n_students, n_schools, additions):
    '''
    Finds a bad edge in the sample sublist if there is one.
    '''
    #Sample the full list of preferences
    student_f_pref, school_f_pref = marriage_market_preference_lists(n_students, n_schools)

    student_pre = {}
    school_pre = {}
    student_M = {}
    school_M = {}
    
    student_pre[k], school_pre[k] = restricted_market(k, student_f_pref, school_f_pref)
    student_M[k], school_M[k] = gale_shapley_modified(n_students, n_schools, student_pre[k], school_pre[k])
    bad_edge = search_bad_edge(student_pre[k], school_pre[k], student_f_pref, school_f_pref, student_M[k])
    
    for j in range(1,additions+1):
        if bad_edge == False:
            k_prev = k
            k = k + Delta
            print('working on sublist size: ' + str(k))
            student_pre[k], school_pre[k] = increase_preference_sublist(Delta, student_pre[k_prev], school_pre[k_prev], student_f_pref, school_f_pref)
            student_M[k], school_M[k] = gale_shapley_modified(n_students, n_schools, student_pre[k], school_pre[k])
            bad_edge = search_bad_edge(student_pre[k], school_pre[k], student_f_pref, school_f_pref, student_M[k])
        else: 
            break
    return bad_edge


def mc_simulations_bad_sample(Delta, sublist, additions, n_students, n_schools, iterations):
    '''
    Function
    '''
    bad_sample = {}

    for i in range(iterations):
        print('Working on sample: ' + str(i))

        bad_sample[i] = bad_edges(Delta, sublist, n_students, n_schools, additions)

    total_bad_samples = sum(1 for v in bad_sample.values() if v==True)

    return (total_bad_samples)


def search_all_bad_edges(student_preferences, school_preferences, student_full_preferences, school_full_preferences, student_Match):
    ''' 
    Inputs
    '''

    n_students = len(student_preferences.keys())
    n_schools = len(school_preferences.keys())

    student_preferences_2 = dict(student_preferences)
    school_preferences_2 = dict(school_preferences)
    school_possible_partners = {school: pref[:, 1] for school, pref in school_preferences.items()}

    bad_e_list = []
    
    for student, prefs in student_preferences.items():
        student_full_prefs = student_full_preferences[student]
        student_full_prefs_rows = student_full_prefs.view([('', student_full_prefs.dtype)] * student_full_prefs.shape[1])
        prefs_rows = prefs.view([('', prefs.dtype)] * prefs.shape[1])
        potential_additions = np.setdiff1d(student_full_prefs_rows, prefs_rows).view(student_full_prefs.dtype).reshape(-1, student_full_prefs.shape[1])
        for new_edge in potential_additions:
            s_prefs_restricted = np.vstack((prefs, new_edge))
            student_preferences_2[student] = s_prefs_restricted[s_prefs_restricted[:,0].argsort()]

            sch = new_edge[1]
            school_possible_partners[sch] = np.append(school_possible_partners[sch], student)
            h_prefs = school_full_preferences[sch]
            school_preferences_2[sch] = h_prefs[np.in1d(h_prefs[:,1], school_possible_partners[sch])]

            student_M, school_M = gale_shapley_modified(n_students, n_schools, student_preferences_2, school_preferences_2)
            
            ## Measure change on stable match

            bad_e = change_original_rank_bad_edge(student_Match, student_M)
            if bad_e == False:
                bad_e_list.append(0)
            else: 
                bad_e_list.append(1)
                #print(student)
                #print(new_edge)
                #print(student_M)

    number_bad_edges = sum(bad_e_list)
    total_edges = len(bad_e_list)
    bad_edges_prop = number_bad_edges/total_edges

    return bad_edges_prop



def all_bad_edges(Delta, k, n_students, n_schools, additions):
    '''
    Finds a bad edge in the sample sublist if there is one.
    '''
    #Sample the full list of preferences
    student_f_pref, school_f_pref = marriage_market_preference_lists(n_students, n_schools)
    #print('The initial list of preferences:')
    #print(student_f_pref, school_f_pref)

    student_pre = {}
    school_pre = {}
    student_M = {}
    school_M = {}
    bad_edge_p = {}

    student_pre[k], school_pre[k] = restricted_market(k, student_f_pref, school_f_pref)
    #print('The sample k list of preferences:')
    #print(student_pre[k], school_pre[k])
    student_M[k], school_M[k] = gale_shapley_modified(n_students, n_schools, student_pre[k], school_pre[k])
    #print('The initial gale shapley result:')
    #print(student_M[k])
    bad_edge_p[k] = search_all_bad_edges(student_pre[k], school_pre[k], student_f_pref, school_f_pref, student_M[k])
    
    for j in range(1,additions+1):

        k_prev = k
        k = k + Delta
        print('working on sublist size: ' + str(k))
        student_pre[k], school_pre[k] = increase_preference_sublist(Delta, student_pre[k_prev], school_pre[k_prev], student_f_pref, school_f_pref)
        student_M[k], school_M[k] = gale_shapley_modified(n_students, n_schools, student_pre[k], school_pre[k])
        bad_edge_p[k] = search_all_bad_edges(student_pre[k], school_pre[k], student_f_pref, school_f_pref, student_M[k])
        
    return bad_edge_p


def mc_simulations_bad_edges(Delta, sublist, additions, n_students, n_schools, iterations):
    
    end = sublist+Delta*additions + Delta
    
    average_bad_edges_proportion = {x : 0 for x in range(sublist, end, Delta)}
    bad_sample_sum = {i : 0 for i in range(iterations)}
    bad_sample = {}

    for i in range(iterations):
        print('Working on sample: ' + str(i))

        bad_edges_proportion = all_bad_edges(Delta, sublist, n_students, n_schools, additions)

        for size, value in bad_edges_proportion.items():
            average_bad_edges_proportion[size] += value/iterations
            bad_sample_sum[i] += value
        if bad_sample_sum[i] > 0: 
            bad_sample[i] = 1
        else: 
            bad_sample_sum[i] = 0

    total_bad_samples = sum(1 for v in bad_sample.values() if v==1)

    return average_bad_edges_proportion, total_bad_samples


##########################################
# TOP Trading cycles and Pareto Optimality
##########################################

def find_cycles(unmatched_students, unmatched_schools, next_student_choice, next_school_choice, student_preferences, school_preferences, student_match):
    potential_match_student = np.copy(student_match)
    n_schools = len(next_school_choice)
    potential_match_school = [-1] * n_schools
    candidate_students = []

    for student in unmatched_students:
        student_pref  = np.copy(student_preferences[student])
        while next_student_choice[student] < student_preferences[student].shape[0]:
            if student_pref[next_student_choice[student]][1] in unmatched_schools:
                potential_match_student[student] = student_pref[next_student_choice[student]]
                candidate_students.append(student)
                break
            else:
                next_student_choice[student] += 1

    for school in unmatched_schools:
        school_pref  = np.copy(school_preferences[school])
        while next_school_choice[school] < school_preferences[school].shape[0]:
            if school_pref[next_school_choice[school]][1] in unmatched_students:
                potential_match_school[school] = school_pref[next_school_choice[school]][1]
                break
            else:
                next_school_choice[school] += 1

    visited = set()
    cycles = []

    for start_student in candidate_students:
        
        if start_student in visited:
            continue

        path_students = [start_student]
        school = potential_match_student[start_student][1]
        path_schools = [school]
        next_student = potential_match_school[school]

        loop_break = 0
        while next_student not in path_students:
            if next_student in visited:
                loop_break = 1
                break
            else:
                path_students.append(next_student)
                next_school = potential_match_student[next_student][1]
                path_schools.append(next_school)
                next_student = potential_match_school[next_school]
        
        if loop_break == 0:
            cycle = []
            for stud in reversed(path_students):
                cycle.insert(0,stud)
                if stud == next_student:
                    break
            cycles.append(cycle)
            visited |= set(path_students)
        else:
            visited |= set(path_students)

    return cycles, potential_match_student

def top_trading_cycles(n_students, n_schools, student_preferences, school_preferences):
    
    unmatched_students = list(range(n_students))
    unmatched_schools = list(range(n_schools))
    np.random.shuffle(unmatched_students)
    np.random.shuffle(unmatched_schools)

    student_match = np.full((n_students, 2), -9999, dtype=int)
    school_match = np.full((n_schools, 2), -9999, dtype=int)

    next_student_choice = [0] * n_students
    next_school_choice = [0] * n_schools
    
    while unmatched_students: 
        
        cycl, p_stud_match = find_cycles(unmatched_students, unmatched_schools, next_student_choice, next_school_choice, student_preferences, school_preferences, student_match)

        if not cycl:
            break
        else:
            for cycle in cycl:
                for student in cycle: 
                    match = p_stud_match[student]
                    school = match[1]
                    student_match[student] = match
                    school_pre = school_preferences[school]
                    school_match[school] = np.copy(school_pre[school_pre[:,1] == student])
                    unmatched_students.remove(student)
                    unmatched_schools.remove(school)                  
    return student_match, school_match

def simulation_matching_increase_preferences_ttc(Delta, k, n_students, n_schools, additions):
    '''
    Simulates the matching outcome under diferent preference list sizes where we only add new preferences
    by using the ttc algorithm.
    '''
    student_f_pref, school_f_pref = marriage_market_preference_lists(n_students, n_schools)

    student_pre = {}
    school_pre = {}
    student_M = {}
    school_M = {}
    
    student_pre[k], school_pre[k] = restricted_market(k, student_f_pref, school_f_pref)
    student_M[k], school_M[k] = top_trading_cycles(n_students, n_schools, student_pre[k], school_pre[k])
    
    for j in range(1,additions+1):
        k_prev = k
        k = k + Delta
        print('working on sublist size: ' + str(k))
        student_pre[k], school_pre[k] = increase_preference_sublist(Delta, student_pre[k_prev], school_pre[k_prev], student_f_pref, school_f_pref)
        student_M[k], school_M[k] = top_trading_cycles(n_students, n_schools, student_pre[k], school_pre[k])
        
    return student_M, school_M, student_f_pref, school_f_pref


def mc_simulations_utility_ttc(Delta, sublist, additions, n_students, n_schools, iterations):
    '''
    Function to simulate the behaviour of different utility functions on the stable match
    outcome with different sublist sizes.
    '''
    beg = sublist + Delta
    end = sublist+Delta*additions + Delta
    
    average_nash_welfare_students = {x : 0 for x in range(sublist, end, Delta)}
    average_nash_welfare_schools = {x : 0 for x in range(sublist, end, Delta)}

    average_leontief_utility = {x : 0 for x in range(sublist, end, Delta)} 
    average_cobb_stone_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_qlinear_power_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_qlinear_square_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_miscelaneous_1_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_miscelaneous_2_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_miscelaneous_3_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_exponential_utility = {x : 0 for x in range(sublist, end, Delta)}
    average_s_shape_utility = {x : 0 for x in range(sublist, end, Delta)}
    

    average_oranks_students = {x : 0 for x in range(sublist, end, Delta)}
    average_oranks_schools = {x : 0 for x in range(sublist, end, Delta)}
    ranks_students = {x : [] for x in range(sublist, end, Delta)}
    ranks_schools = {x : [] for x in range(sublist, end, Delta)}
    r_profile = {x : np.zeros(n_schools+1) for x in range(sublist, end, Delta)}


    for i in range(iterations):
        print('Working on iteration: ' + str(i))

        student_Match, school_Match, student_original_preferences, school_original_preferences = simulation_matching_increase_preferences_ttc(Delta, sublist, n_students, n_schools, additions)

        nash_welfare_students, nash_welfare_schools = nash_welfare(student_Match, school_Match)
        mean_original_ranks_students, mean_original_ranks_schools, or_students, or_schools = average_rank_match(student_Match, school_Match)
        ranks_profile = rank_profile(student_Match, school_Match)
        (leontief_u, cobb_stone_u, qlinear_power_u, qlinear_square_u, 
        miscelaneous_1_u, miscelaneous_2_u, miscelaneous_3_u,
        exponential_u, s_shape_u) = utility_functions(student_Match, school_Match, ranks_profile)


        #Students
        for size, value in nash_welfare_students.items():
            average_nash_welfare_students[size] += value/iterations

        for size, value in mean_original_ranks_students.items():
            average_oranks_students[size] += value/iterations 

        for size, ary in or_students.items():
            ranks_students[size].extend(ary)
        
        for size, rk_profile in ranks_profile.items():
            r_profile[size] = r_profile[size] + rk_profile/iterations  
        
        for size, value in leontief_u.items():
            average_leontief_utility[size] += value/iterations

        for size, value in cobb_stone_u.items():
            average_cobb_stone_utility[size] += value/iterations

        for size, value in qlinear_power_u.items():
            average_qlinear_power_utility[size] += value/iterations

        for size, value in qlinear_square_u.items():
            average_qlinear_square_utility[size] += value/iterations

        for size, value in miscelaneous_1_u.items():
            average_miscelaneous_1_utility[size] += value/iterations
        
        for size, value in miscelaneous_2_u.items():
            average_miscelaneous_2_utility[size] += value/iterations

        for size, value in miscelaneous_3_u.items():
            average_miscelaneous_3_utility[size] += value/iterations
        
        for size, value in exponential_u.items():
            average_exponential_utility[size] += value/iterations

        for size, value in s_shape_u.items():
            average_s_shape_utility[size] += value/iterations 

        #Schools

        for size, value in nash_welfare_schools.items():
            average_nash_welfare_schools[size] += value/iterations

        for size, value in mean_original_ranks_schools.items():
            average_oranks_schools[size] += value/iterations

        for size, ary in or_schools.items():
            ranks_schools[size].extend(ary)

    return (average_nash_welfare_students, average_nash_welfare_schools, 
    average_oranks_students, average_oranks_schools,
    ranks_students, ranks_schools, 
    r_profile, 
    average_leontief_utility, average_cobb_stone_utility, 
    average_qlinear_power_utility, average_qlinear_square_utility, 
    average_miscelaneous_1_utility, average_miscelaneous_2_utility,
    average_miscelaneous_3_utility, average_exponential_utility,
    average_s_shape_utility)


##################################################################
## Pareto Optimality in Gale Shapley output
##################################################################

def trade_in_free(student_match, school_match, student_prefs):
    school_mat = np.array(school_match[:, 1]) 
    unmatched_schools = np.where(school_mat == -9999)
    trade_free = True
    for student in range(len(student_match)):
        student_preferences = student_prefs[student]
        for school in unmatched_schools:
            potential_match = student_preferences[student_preferences[:, 1] == school][0]
            if len(potential_match)>0:
                if student_match[student, 0] > potential_match[0]:
                    trade_free = False 
                    break 
        if trade_free == False: 
            break

    return trade_free

def coalition_free(student_match, school_match, student_prefs):   
    coalition_f = True

    n_students = len(student_match)
    n_schools = len(school_match)

    candidate_students = list(range(n_students))
    candidate_schools = list(range(n_schools))

    next_student_choice = [0] * n_students

    first_on_list = True
    while (first_on_list==True and len(candidate_students)>0):
        for student in candidate_students:
            student_pref  = np.copy(student_prefs[student])
            if next_student_choice[student] < student_pref.shape[0]:
                sch = student_pref[next_student_choice[student]][1]
                if sch in candidate_schools:
                    if student_match[student][1] == sch:
                        candidate_students.remove(student)
                        candidate_schools.remove(sch)
                    else: 
                        first_on_list = False
                else:
                    next_student_choice[student] += 1
            else:
                candidate_students.remove(student)


    if len(candidate_students)>0:

        visited = set()
        cycles = []

        for start_student in candidate_students:
            
            if start_student in visited:
                continue

            path_students = [start_student]
            student_pref  = student_prefs[start_student]
            school = student_pref[next_student_choice[start_student]][1]
            path_schools = [school]
            next_student = school_match[school]

            loop_break = 0
            while next_student not in path_students:
                if next_student in visited:
                    loop_break = 1
                    break
                else:
                    path_students.append(next_student)
                    student_pref  = student_prefs[next_student]
                    next_school = student_pref[next_student_choice[next_student]][1]
                    path_schools.append(next_school)
                    next_student = school_match[next_school]
            
            if loop_break == 0:
                cycle = []
                for stud in reversed(path_students):
                    cycle.insert(0,stud)
                    if stud == next_student:
                        break
                cycles.append(cycle)
                visited |= set(path_students)
            else:
                visited |= set(path_students)
        
        if len(cycles)>0:
            for cycle in cycles:
                if len(cycle)>1:
                    coalition_f = False
                    break 

    return coalition_f


def is_pareto_optimal(student_match, school_match, student_prefs):
    
    pareto = False

    t_in_free = trade_in_free(student_match, school_match)

    if t_in_free == True: 
        c_free = coalition_free(student_match, school_match, student_prefs)
        if c_free == True:
            pareto = True
        
    return pareto

