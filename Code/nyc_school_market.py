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