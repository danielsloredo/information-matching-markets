
from unittest import skip
import numpy as np
import random as ra
import unbalanced_matching as um
import counselor_matching as cm

def changeMatch(student_sp, school_sp, student_sp_2, school_sp_2):
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

    return total_student_changes, total_school_changes


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

    for extra_schools in schools_to_add:
        print('simulating with addittion to preferences of : ' + str(extra_schools))
        num_student_sp_changes = []
        num_school_sp_changes = []

        for i in range(iter):
            if i % 10 == 0:
                print('working on iteration: ' + str(i))

            student_pref, school_pref = um.simulationMarriageMarket(n_students, n_schools, student_pref_sizes, school_pref_size)
            student_pref_2, school_pref_2, candidates = cm.counselorIncreasePreferences(students_to_modify, extra_schools, student_pref, school_pref, counselor_confidence)
            student_sp, school_sp = cm.galeShapleyModified(n_students, n_schools, student_pref, school_pref)
            student_sp_2, school_sp_2 = cm.galeShapleyModified(n_students, n_schools, student_pref_2, school_pref_2)
            print(student_sp==student_sp_2)
            print(school_sp==student_sp_2)

            total_student_ch, total_school_ch = changeMatch(student_sp, school_sp, student_sp_2, school_sp_2)

            num_student_sp_changes.append(total_student_ch)
            num_school_sp_changes.append(total_school_ch)

        student_change[extra_schools] = sum(num_student_sp_changes)/iter
        school_change[extra_schools] = sum(num_school_sp_changes)/iter
        
    return student_change, school_change
