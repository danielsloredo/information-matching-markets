from unittest import skip
import numpy as np
import random as ra

def MarriageMarketPreferenceLists(n_students, n_schools):

    students = [i for i in range(n_students)]
    schools = [i for i in range(n_schools)]

    student_full_preferences = {}
    school_full_preferences = {}

    for student in students: 
        student_full_preferences[student] = np.random.choice(schools, n_schools, replace=False).tolist()
    for school in schools: 
        school_full_preferences[school] = np.random.choice(students, n_students, replace = False).tolist()

    return student_full_preferences, school_full_preferences

def RestrictedMarket(d_student, student_full_preferences, school_full_preferences):

    student_preferences = {}
    school_preferences = {}

    for student in studen:
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



def simulationMarriageMarket(n_students, n_schools, d_student, d_school):
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

    students = [i for i in range(n_men)]
    schools = [i for i in range(n_women)]


    student_preferences = {}
    school_preferences = {}

    for student in students:
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