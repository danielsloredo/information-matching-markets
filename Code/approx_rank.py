import numpy as np
import math
from scipy.stats import hypergeom
from itertools import product
'''
def expected_rank_sublist_student_prev_approx(sublist, student, n_schools):
    expected_rank = 0
    sum_to_overlap = np.min([sublist + 1, student])

    for matched_schools in range(1, student):
        if matched_schools == student - 1:
            p_matched_schools = 1
        else:
            p_matched_schools = 0
        for overlaps in range(sum_to_overlap):
            expected_rank += (n_schools+1)/(sublist-overlaps+1) * hypergeom.pmf(overlaps, n_schools, sublist, matched_schools) * p_matched_schools   
    return expected_rank


def expected_rank_sublist_student_test(sublist, student, n_schools):
    expected_rank = 0
    sum_to_overlap = np.min([sublist + 1, student])
    print('working on student ' + str(student))
    for matched_schools in range(1, student):
        print('working on matched schools ' + str(matched_schools))
        if (student - 1 <= sublist) & (matched_schools == student - 1):
            p_matched_schools = 1
        elif matched_schools < sublist:
            p_matched_schools = 0
        else:
            coef = float(math.comb(n_schools, matched_schools))
            inner_sum = 0 
            for l in range(matched_schools - sublist + 1):
                left_comb = float(math.comb(matched_schools, l))
                inner_right_comb = float(math.comb(matched_schools - l, sublist)/math.comb(n_schools, sublist))
                right_comb = np.power(inner_right_comb,(student - 1))
                inner_sum += np.power(-1,l)  * left_comb * right_comb
            p_matched_schools = coef * inner_sum

        for overlaps in range(sum_to_overlap):
            expected_rank += (n_schools+1)/(sublist-overlaps+1) * hypergeom.pmf(overlaps, n_schools, sublist, matched_schools) * p_matched_schools   
        print('the expected rank is ')
        print(expected_rank)
    return expected_rank

def expected_rank_sublist_student(sublist, student, n_schools):
    expected_rank = 0
    sum_to_overlap = np.min([sublist + 1, student])

    if sublist >= student - 1:
        for overlaps in range(sum_to_overlap):
            expected_rank += (n_schools+1)/(sublist-overlaps+1) * hypergeom.pmf(overlaps, n_schools, sublist, student - 1)
    else:
        cum_prob = 0 
        for matched_schools in range(sublist, student):
            if matched_schools < student - 1:
                coef = float(math.comb(n_schools, matched_schools))
                inner_sum = 0 
                for l in range(matched_schools - sublist + 1):
                    left_comb = float(math.comb(matched_schools, l))
                    inner_right_comb = float(math.comb(matched_schools - l, sublist)/math.comb(n_schools, sublist))
                    right_comb = np.power(inner_right_comb,(student - 1))
                    inner_sum += np.power(-1,l)  * left_comb * right_comb
                p_matched_schools = coef * inner_sum
                cum_prob += p_matched_schools

                for overlaps in range(sum_to_overlap):
                    expected_rank += (n_schools+1)/(sublist-overlaps+1) * hypergeom.pmf(overlaps, n_schools, sublist, matched_schools) * p_matched_schools   
            else:
                for overlaps in range(sum_to_overlap):
                    expected_rank += (n_schools+1)/(sublist-overlaps+1) * hypergeom.pmf(overlaps, n_schools, sublist, student - 1) * (1-cum_prob)

    return expected_rank


def expected_ranks_sublist(sublist, n_students, n_schools):
    index_students = list(range(n_students)) 
    expected_ranks = np.zeros(n_students) 

    expected_ranks[0] = (n_schools+1)/(sublist+1)
    for index_std in index_students[1:]:
        expected_ranks[index_std] = expected_rank_sublist_student(sublist, index_std+1, n_schools)

    return expected_ranks

def nash_welfare(student_ranks, n_schools): 

    ranks = np.copy(student_ranks)
    utility = np.array(n_schools+2-ranks, dtype=float)
    nash_welfare_students = np.power(utility.prod(),(1/student_ranks.shape[0]))
        
    return nash_welfare_students

def simulation_ranks(initial_sublist, additions, delta, n_students, n_schools):
    
    end = initial_sublist+delta*additions + delta

    ranks_students = {}
    average_oranks_students = {x : 0 for x in range(initial_sublist, end, delta)}
    nash_welfare_students = {x : 0 for x in range(initial_sublist, end, delta)}
    
    for sublist_size in range(initial_sublist, end, delta):
        print('working on sublist size: ' + str(sublist_size))
        ranks_students_size = expected_ranks_sublist(sublist_size, n_students, n_schools)
        ranks_students[sublist_size] = ranks_students_size
        average_oranks_students[sublist_size] = ranks_students_size.mean()
        nash_welfare_students[sublist_size] = nash_welfare(ranks_students_size, n_schools)
    
    return ranks_students, average_oranks_students, nash_welfare_students
'''
#############################################################################################
#############################################################################################
#Approximation Formula
#
#############################################################################################
#############################################################################################


def expected_min_rank_overlaps(sublist, student, matched, n_schools):
    sum_to_overlap = np.min([sublist+1, student])

    expected_min = np.zeros(sum_to_overlap)
    overlap_prob = np.zeros(sum_to_overlap)

    for overlap in range(sum_to_overlap):
        expected_min[overlap] = (n_schools+1)/(sublist-overlap+1)
        overlap_prob[overlap] = hypergeom.pmf(overlap, n_schools, sublist, matched)

    sum_expected_overlap = np.sum(expected_min * overlap_prob)
    return sum_expected_overlap

def probability_matched(sublist, student, matched, n_schools):
    
    w_d_l = np.zeros(matched - sublist)
    
    if len(w_d_l) == 0:
        product_w_d_l = 1
    else:
        for l in range(sublist, matched):
            w_d_l[l-sublist] = 1 - hypergeom.pmf(sublist, n_schools, sublist, l)
        product_w_d_l = np.product(w_d_l)

    t_values_function = lambda n,t:[k for k in product(range(t+1),repeat=n) if sum(k)==t]

    t_values = t_values_function(matched-sublist+1, student - 1 - matched)

    path = 0
    path_probability = np.zeros(len(t_values))
    for t_values_path in t_values:
        step_prob = np.zeros(matched - sublist + 1)
        for j in range(sublist, matched + 1):
            step_prob[j - sublist] = hypergeom.pmf(sublist, n_schools, sublist, j)
        path_probabilities = np.power(step_prob, t_values_path)
        path_probability[path] = np.prod(path_probabilities)
        path += 1

    path_probs_sum = np.sum(path_probability)
    
    
    probability_k_match = product_w_d_l * path_probs_sum
    #print('The probability diagonal for mathced '+str(matched)+' for student '+str(student)+' is of '+str(product_w_d_l))
    #print('The probability path for matched '+str(matched)+' for student '+str(student)+' is of '+str(path_probs_sum))
    #print('The probability of matched '+str(matched)+' for student '+str(student)+' is of '+str(probability_k_match))
    return probability_k_match

def expected_rank_student_sublist(sublist, student, n_schools):
    E_rank_i_d = 0

    if student-1 <= sublist:
        E_rank_i_d = expected_min_rank_overlaps(sublist, student, student-1, n_schools)
    else:
        for k in range(sublist, student):
            E_rank_i_d += probability_matched(sublist,student, k, n_schools) * expected_min_rank_overlaps(sublist, student, k, n_schools)
    #print('The expected rank for  '+str(student)+' is of '+ str(E_rank_i_d))
    return E_rank_i_d


def expected_ranks_sublist(sublist, n_students, n_schools):
    index_students = list(range(n_students)) 
    expected_ranks = np.zeros(n_students) 

    expected_ranks[0] = (n_schools+1)/(sublist+1)

    for index_std in index_students[1:]:
        expected_ranks[index_std] = expected_rank_student_sublist(sublist, index_std+1, n_schools)

    return expected_ranks

def nash_welfare(student_ranks, n_schools): 

    ranks = np.copy(student_ranks)
    utility = np.array(n_schools+2-ranks, dtype=float)
    nash_welfare_students = np.power(utility.prod(),(1/student_ranks.shape[0]))
        
    return nash_welfare_students

def simulation_ranks(initial_sublist, additions, delta, n_students, n_schools):
    
    end = initial_sublist+delta*additions + delta

    ranks_students = {}
    average_oranks_students = {x : 0 for x in range(initial_sublist, end, delta)}
    nash_welfare_students = {x : 0 for x in range(initial_sublist, end, delta)}
    
    for sublist_size in range(initial_sublist, end, delta):
        print('working on sublist size: ' + str(sublist_size))
        ranks_students_size = expected_ranks_sublist(sublist_size, n_students, n_schools)
        ranks_students[sublist_size] = ranks_students_size
        average_oranks_students[sublist_size] = ranks_students_size.mean()
        nash_welfare_students[sublist_size] = nash_welfare(ranks_students_size, n_schools)
    
    return ranks_students, average_oranks_students, nash_welfare_students
