
from unittest import skip
import numpy as np
import random as ra
import unbalanced_matching as um
import counselor_matching as cm

def changeMatch(student_sp, school_sp, student_sp_2, school_sp_2):
    '''
    Function that registers if the student or school changed stable partner after adding schools to the preference list
    '''
    difference_student = [None] * len(student_sp)
    for index in range(len(student_sp)):
        if student_sp[index] == student_sp_2[index]:
            difference_student[index] = 0
        else:
            difference_student[index] = 1
    difference_school = [None] * len(school_sp)
    for index in range(len(school_sp)):
        if school_sp[index] == school_sp_2[index]:
            difference_school[index] = 0
        else:
            difference_school[index] = 1

    total_student_changes = sum(difference_student)
    total_school_changes = sum(difference_school)

    return total_student_changes, total_school_changes, difference_student, difference_school

def averageTrueRankPartnersModified(student_spouse, school_spouse, student_preferences, school_preferences, student_preferences_2, school_preferences_2, differences_students, differences_schools, modified_candidates):
    '''
    Function that computes the average rank of partners in the stable match taking into acount if there is a difference in match after adding extra schools to list
    INPUT:
        student_spouse: list with stable partners for students
        school_spouse: list with stable partners for schools
        student_preferences: dictionary with the list of preferences for each one of the students
        school_preferences: dictionary with the list of preferences for each one of the schools
        modified_candidates: list with students that received advice from a counselor
    Output: 
        school_average_rank: average rank of partners for schools in the stable match
        candidates_average_rank: average rank of partners for modified students in the stable match
        noncandidates_average_rank: average rank of partners for non-modified students in the stable match
    '''    
    student_ranks = {}
    school_ranks = {}

    for student, prefs in student_preferences.items():
        if differences_students[student] == 0:
            if student_spouse[student] == None:
                student_rank_unmatched = len(student_preferences[student]) + 1
                student_ranks[student] = student_rank_unmatched
            else:
                student_ranks[student] = prefs.index(student_spouse[student]) + 1
        else:
            if student_spouse[student] == None:
                student_rank_unmatched = len(student_preferences_2[student]) + 1
                student_ranks[student] = student_rank_unmatched
            else:
                prefs_2 = student_preferences_2[student]
                student_ranks[student] = prefs_2.index(student_spouse[student]) + 1
    
    for school, prefs in school_preferences.items():
        if differences_schools[school] == 0:
            if school_spouse[school] == None:
                if school_preferences[school] != None:
                    school_rank_unmatched = len(school_preferences[school]) + 1
                    school_ranks[school] = school_rank_unmatched
                else:
                    skip
            else:
                school_ranks[school] = prefs.index(school_spouse[school]) + 1
        else:
            if school_spouse[school] == None:
                school_rank_unmatched = len(school_preferences_2[school]) + 1
                school_ranks[school] = school_rank_unmatched
            else:
                prefsS_2 = school_preferences_2[school]
                school_ranks[school] = prefsS_2.index(school_spouse[school]) + 1


    noncandidates = list(set(student_preferences.keys()).difference(modified_candidates)) 
    candidate_ranks = {cand: student_ranks[cand] for cand in modified_candidates}
    candidates_average_rank = sum(candidate_ranks.values())/len(modified_candidates)    
    noncandidate_ranks = {cand: student_ranks[cand] for cand in noncandidates}
    noncandidates_average_rank = sum(noncandidate_ranks.values())/len(noncandidates)

    school_average_rank = sum(school_ranks.values())/len(list(school_preferences.keys()))

    return school_average_rank, candidates_average_rank, noncandidates_average_rank

def simulationTrueChange(n_students, n_schools, student_pref_sizes, school_pref_size, students_to_modify, schools_to_add, counselor_confidence, iter):
    '''
    Function to simulate the average ranks of partners for both sides of a matching market 
    with heterogeneous sizes on preferences lists for some of the agents
    INPUT:
        n_students: number of students in the market
        n_schools: number of schools in the market
        student_pref_sizes: list with sizes for the preference list of students
        school_pref_size: size of the preference list for schools
        students_to_modify: number of students to modify in the market
        schools_to_add: number of schools to add to the preference lists of the modified students
        iter: number of iterations in the simulation
    Output: 
        school_rank: average rank of partners for schools in the stable match
        candidates_rank: average rank of partners for modified students in the stable match
        noncandidates_rank: average rank of partners for non-modified students in the stable match
    '''

    student_change = {}
    school_change = {}

    rank_candidates = {}
    rank_school = {}
    rank_noncandidates = {}

    for extra_schools in schools_to_add:
        print('simulating with addittion to preferences of : ' + str(extra_schools))
        num_student_sp_changes = []
        num_school_sp_changes = []

        candidate_average_ranks = []
        school_average_ranks = []
        noncandidates_average_ranks = []

        for i in range(iter):
            if i % 10 == 0:
                print('working on iteration: ' + str(i))

            student_pref, school_pref = um.simulationMarriageMarket(n_students, n_schools, student_pref_sizes, school_pref_size)
            student_pref_2, school_pref_2, candidates = cm.counselorIncreasePreferences(students_to_modify, extra_schools, student_pref, school_pref, counselor_confidence)
            student_sp, school_sp = cm.galeShapleyModified(n_students, n_schools, student_pref, school_pref)
            student_sp_2, school_sp_2 = cm.galeShapleyModified(n_students, n_schools, student_pref_2, school_pref_2)

            total_student_ch, total_school_ch, diff_student, diff_school = changeMatch(student_sp, school_sp, student_sp_2, school_sp_2)
            num_student_sp_changes.append(total_student_ch)
            num_school_sp_changes.append(total_school_ch)

            school_average_r, candidate_av_rank, noncandidates_av_rank = averageTrueRankPartnersModified(student_sp_2, school_sp_2, student_pref, school_pref, student_pref_2, school_pref_2, diff_student, diff_school, candidates)
            candidate_average_ranks.append(candidate_av_rank)
            school_average_ranks.append(school_average_r)
            noncandidates_average_ranks.append(noncandidates_av_rank)
            
        rank_school[extra_schools] = sum(school_average_ranks)/iter
        rank_candidates[extra_schools] = sum(candidate_average_ranks)/iter
        rank_noncandidates[extra_schools] = sum(noncandidates_average_ranks)/iter

        student_change[extra_schools] = sum(num_student_sp_changes)/iter
        school_change[extra_schools] = sum(num_school_sp_changes)/iter
        
    return student_change, school_change, rank_school, rank_candidates, rank_noncandidates


def averageTrueRankDifferences(student_spouse, school_spouse, student_preferences, school_preferences, student_preferences_2, school_preferences_2, differences_students, differences_schools, modified_candidates):
    '''
    INPUT:
        student_spouse: list with stable partners for students
        school_spouse: list with stable partners for schools
        student_preferences: dictionary with the list of preferences for each one of the students
        school_preferences: dictionary with the list of preferences for each one of the schools
        modified_candidates: list with students that received advice from a counselor
    Output: 
        school_average_rank: average rank of partners for schools in the stable match
        candidates_average_rank: average rank of partners for modified students in the stable match
        noncandidates_average_rank: average rank of partners for non-modified students in the stable match
    '''    
    student_ranks = {}
    student_ranks_diff = {}
    school_ranks = {}
    school_ranks_diff = {}

    for student, prefs in student_preferences.items():
        if differences_students[student] == 0:
            if student_spouse[student] == None:
                student_rank_unmatched = len(student_preferences[student]) + 1
                student_ranks[student] = student_rank_unmatched
            else:
                student_ranks[student] = prefs.index(student_spouse[student]) + 1
        else:
            if student_spouse[student] == None:
                student_rank_unmatched = len(student_preferences_2[student]) + 1
                student_ranks_diff[student] = student_rank_unmatched
            else:
                prefs_2 = student_preferences_2[student]
                student_ranks_diff[student] = prefs_2.index(student_spouse[student]) + 1
    
    for school, prefs in school_preferences.items():
        if differences_schools[school] == 0:
            if school_spouse[school] == None:
                if school_preferences[school] != None:
                    school_rank_unmatched = len(school_preferences[school]) + 1
                    school_ranks[school] = school_rank_unmatched
                else:
                    skip
            else:
                school_ranks[school] = prefs.index(school_spouse[school]) + 1
        else:
            if school_spouse[school] == None:
                school_rank_unmatched = len(school_preferences_2[school]) + 1
                school_ranks_diff[school] = school_rank_unmatched
            else:
                prefsS_2 = school_preferences_2[school]
                school_ranks_diff[school] = prefsS_2.index(school_spouse[school]) + 1


    #noncandidates = list(set(student_preferences.keys()).difference(modified_candidates)) 
    #candidate_ranks = {cand: student_ranks[cand] for cand in modified_candidates}
    #candidates_average_rank = sum(candidate_ranks.values())/len(modified_candidates)    
    #noncandidate_ranks = {cand: student_ranks[cand] for cand in noncandidates}
    #noncandidates_average_rank = sum(noncandidate_ranks.values())/len(noncandidates)

    st_average_rank = sum(student_ranks.values())/(len(list(student_ranks.keys()))+.0001)
    stdiff_average_rank = sum(student_ranks_diff.values())/(len(list(student_ranks_diff.keys()))+.0001)    
    sc_average_rank = sum(school_ranks.values())/(len(list(school_ranks.keys()))+.0001)
    scdiff_average_rank = sum(school_ranks_diff.values())/(len(list(school_ranks_diff.keys()))+.0001)

    return st_average_rank, stdiff_average_rank, sc_average_rank, scdiff_average_rank    


def simulationTrueChangeDifferences(n_students, n_schools, student_pref_sizes, school_pref_size, students_to_modify, schools_to_add, counselor_confidence, iter):
    '''
  
    INPUT:
        n_students: number of students in the market
        n_schools: number of schools in the market
        student_pref_sizes: list with sizes for the preference list of students
        school_pref_size: size of the preference list for schools
        students_to_modify: number of students to modify in the market
        schools_to_add: number of schools to add to the preference lists of the modified students
        iter: number of iterations in the simulation
    Output: 
        school_rank: average rank of partners for schools in the stable match
        candidates_rank: average rank of partners for modified students in the stable match
        noncandidates_rank: average rank of partners for non-modified students in the stable match
    '''

    #student_change = {}
    #school_change = {}

    rank_student = {}
    rank_student_diff = {}
    rank_school = {}
    rank_school_diff = {}

    for extra_schools in schools_to_add:
        print('simulating with addittion to preferences of : ' + str(extra_schools))
        #num_student_sp_changes = []
        #num_school_sp_changes = []

        student_average_rank = [] 
        student_average_rank_diff = []
        school_average_rank = []
        school_average_rank_diff = []

        for i in range(iter):
            if i % 10 == 0:
                print('working on iteration: ' + str(i))

            student_pref, school_pref = um.simulationMarriageMarket(n_students, n_schools, student_pref_sizes, school_pref_size)
            student_pref_2, school_pref_2, candidates = cm.counselorIncreasePreferences(students_to_modify, extra_schools, student_pref, school_pref, counselor_confidence)
            student_sp, school_sp = cm.galeShapleyModified(n_students, n_schools, student_pref, school_pref)
            student_sp_2, school_sp_2 = cm.galeShapleyModified(n_students, n_schools, student_pref_2, school_pref_2)

            total_student_ch, total_school_ch, diff_student, diff_school = changeMatch(student_sp, school_sp, student_sp_2, school_sp_2)
            #num_student_sp_changes.append(total_student_ch)
            #num_school_sp_changes.append(total_school_ch)

            student_av_rank, student_av_rank_diff, school_av_rank, school_av_rank_diff = averageTrueRankDifferences(student_sp_2, school_sp_2, student_pref, school_pref, student_pref_2, school_pref_2, diff_student, diff_school, candidates)
            
            student_average_rank.append(student_av_rank)
            student_average_rank_diff.append(student_av_rank_diff)
            school_average_rank.append(school_av_rank)
            school_average_rank_diff.append(school_av_rank_diff)
            
        rank_student[extra_schools] = sum(student_average_rank)/iter
        rank_student_diff[extra_schools] = sum(student_average_rank_diff)/iter
        rank_school[extra_schools] = sum(school_average_rank)/iter
        rank_school_diff[extra_schools] = sum(school_average_rank_diff)/iter

        #student_change[extra_schools] = sum(num_student_sp_changes)/iter
        #school_change[extra_schools] = sum(num_school_sp_changes)/iter
        
    return rank_student, rank_student_diff, rank_school, rank_school_diff