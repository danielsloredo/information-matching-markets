from turtle import color
import numpy as np
import unbalanced_matching as um
import counselor_matching as cm
import real_change_on_rank as rc
import nyc_school_market as nyc
import optim_nyc as onyc
import matplotlib.pyplot as plt
import json
import ast
import sys
import time


'''
################################################################################
# Replication of results and counselor matching
#
################################################################################
men_pref_sizes = list(range(5,151))

rank_size_men, rank_size_women = um.simulationMCMatching(1000, 1001, men_pref_sizes, 1000, 50)

print(rank_size_men)
print(rank_size_women)

lists1 = sorted(rank_size_men.items()) # sorted by key, return a list of tuples
lists2 = sorted(rank_size_women.items())
x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples
x2, y2 = zip(*lists2)
plt.plot(x1, y1, label='Rank_Students')
plt.plot(x2, y2, label='Rank_Schools')
plt.xlabel("Average degree d")
plt.ylabel("Average rank")
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/rank_diff_pref_sizes.png')


schools_extra = list(range(1,50,1))
student_counselor = 50
counselor_conf = .7
rank_schools, rank_candidates, rank_noncandidates = cm.simulationPreferenceAdditions(1000, 1001, 12, 1000, student_counselor, schools_extra, counselor_conf, 50)

print(rank_schools)
print(rank_candidates)
print(rank_noncandidates)


lists2 = sorted(rank_candidates.items()) 
lists3 = sorted(rank_noncandidates.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)
plt.plot(x2, y2, label='Rank_Candidates')
plt.plot(x3, y3, label='Rank_NonCandidates')
plt.xlabel("Extra Schools in preference lists")
plt.ylabel("Average Rank")
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/rank_counselors_2.png')


lists1 = sorted(rank_schools.items()) # sorted by key, return a list of tuples
x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples
plt.plot(x1, y1, label='Rank_Schools')
plt.xlabel("Extra Schools in preference lists")
plt.ylabel("Average Rank")
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/rank_schools_counselors_2.png')


schools_extra = list(range(1,150,5))
student_counselor = 100
counselor_conf = .7
student_total_change, school_total_change, ranks_schools, ranks_candidates, ranks_noncandidates = rc.simulationTrueChange(1000, 1001, 12, 1000, student_counselor, schools_extra, counselor_conf, 50)

print(student_total_change)
print(school_total_change)

print(ranks_schools)
print(ranks_candidates)
print(ranks_noncandidates)

lists2 = sorted(student_total_change.items()) 
lists3 = sorted(school_total_change.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)
plt.figure(1)
plt.plot(x2, y2, label='Student_Changes')
plt.plot(x3, y3, label='School_Changes')
plt.xlabel("Extra Schools in preference lists")
plt.ylabel("Number of Changes in Match")
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/true_change_spouse_100.png')


lists1 = sorted(ranks_schools.items()) # sorted by key, return a list of tuples
x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples
lists3 = sorted(ranks_noncandidates.items())
x3, y3 = zip(*lists3)
plt.figure(2)
plt.plot(x1, y1, label='Rank_Schools')
plt.plot(x3, y3, label='Rank_Students')
plt.xlabel("Extra Schools in preference list")
plt.ylabel("Average Rank")
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/truerank_counselor_100student.png')

schools_extra = list(range(1,150,5))
student_counselor = 100
counselor_conf = .7
ranks_student, ranks_student_diff, ranks_school, ranks_school_diff = rc.simulationTrueChangeDifferences(1000, 1001, 12, 1000, student_counselor, schools_extra, counselor_conf, 50)

lists2 = sorted(ranks_student.items()) 
lists3 = sorted(ranks_student_diff.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)
plt.figure(5)
plt.plot(x2, y2, label='Students same match')
plt.plot(x3, y3, label='Students different match')
plt.xlabel("Extra Schools in preference lists")
plt.ylabel("Average Rank")
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/difference_rank_students100.png')


lists2 = sorted(ranks_school.items()) 
lists3 = sorted(ranks_school_diff.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)
plt.figure(6)
plt.plot(x2, y2, label='Schools same match')
plt.plot(x3, y3, label='Schools different match')
plt.xlabel("Extra Schools in preference lists")
plt.ylabel("Average Rank")
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/difference_rank_schools100.png')
'''


'''
################################################################################
# Simulations of average rank when increasing sublist size 
# Complete list of preferences, additions are sampled from the complete list without replacement
################################################################################
lenght_lists = list(range(10,100,1))

student_pre, student_av_rank, school_pre, school_av_rank = nyc.simulation_matching_market(1000, 1001, lenght_lists, 10)

a_file = open("D:/Documents/CDO/CDO_project/Data/student_preferences.json", "w")
json.dump(student_pre, a_file)
a_file.close()

b_file = open("D:/Documents/CDO/CDO_project/Data/student_average_ranks.json", "w")
json.dump(student_av_rank, b_file)
b_file.close()

c_file = open("D:/Documents/CDO/CDO_project/Data/school_preferences.json", "w")
json.dump(school_pre, c_file)
c_file.close()

d_file = open("D:/Documents/CDO/CDO_project/Data/school_average_ranks.json", "w")
json.dump(school_av_rank, d_file)
d_file.close()


lists2 = sorted(student_av_rank.items()) 
lists3 = sorted(school_av_rank.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)
plt.figure(7)
plt.plot(x2, y2, label="Students' average rank")
plt.plot(x3, y3, label="Schools' average rank")
plt.xlabel("Lenght of student's sampled sub-list")
plt.ylabel("Average Rank of stable partner")
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/ranks_market_same_list_origin1.png')


#a_file = open("D:/Documents/CDO/CDO_project/Data/student_preferences.json", "r")
#student_pre =  a_file.read()
#a_file.close()

b_file = open("D:/Documents/CDO/CDO_project/Data/student_average_ranks.json", "r")
student_av_rank = ast.literal_eval(b_file.read())
b_file.close()

#c_file = open("D:/Documents/CDO/CDO_project/Data/school_preferences.json", "r")
#school_pre = c_file.read()
#c_file.close()

d_file = open("D:/Documents/CDO/CDO_project/Data/school_average_ranks.json", "r")
school_av_rank = ast.literal_eval(d_file.read())
d_file.close()

student_sample_ranks = {k: student_av_rank[k] for k in student_av_rank.keys() & {'10', '15', '20', '25', '30', '35', '40'}}
school_sample_ranks = {k: school_av_rank[k] for k in school_av_rank.keys() & {'10', '14', '20', '26', '30', '35', '40'}}


barWidth = 0.25

lists2 = sorted(student_sample_ranks.items()) 
lists3 = sorted(school_sample_ranks.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)

br2 = np.arange(len(x2))
br3 = [x + barWidth for x in br2]

plt.figure(8)
plt.bar(br2, y2, color = 'royalblue', label="Students' average rank", width=barWidth)
plt.bar(br3, y3, color = 'sandybrown', label="Schools' average rank", width=barWidth)
plt.xlabel("Lenght of student's sampled sub-list")
plt.ylabel("Average Rank of stable partner")
plt.xticks([r + barWidth*.5 for r in range(len(x2))], ['10', '15', '20', '25', '30', '35', '40'])
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/ranks_sample_same_list_origin5.png')

'''

'''
################################################################################
# Simulations of average rank when increasing sublist size of the NYC market approximation
# Complete list of preferences, additions are sampled from the complete list without replacement
################################################################################
lenght_lists = list(range(5,40,1))

student_pre, student_av_rank, school_pre, school_av_rank = nyc.simulation_matching_market(7500, 7300, lenght_lists, 5)

a_file = open("D:/Documents/CDO/CDO_project/Data/student_preferences_realmarket.json", "w")
json.dump(student_pre, a_file)
a_file.close()

b_file = open("D:/Documents/CDO/CDO_project/Data/student_average_ranks_realmarket.json", "w")
json.dump(student_av_rank, b_file)
b_file.close()

c_file = open("D:/Documents/CDO/CDO_project/Data/school_preferences_realmarket.json", "w")
json.dump(school_pre, c_file)
c_file.close()

d_file = open("D:/Documents/CDO/CDO_project/Data/school_average_ranks_realmarket.json", "w")
json.dump(school_av_rank, d_file)
d_file.close()


lists2 = sorted(student_av_rank.items()) 
lists3 = sorted(school_av_rank.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)
plt.figure(7)
plt.plot(x2, y2, label="Students' average rank")
plt.plot(x3, y3, label="Schools' average rank")
plt.xlabel("Lenght of student's sampled sub-list")
plt.ylabel("Average Rank of stable partner")
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/ranks_market_same_list_origin_realmarket.png')


b_file = open("D:/Documents/CDO/CDO_project/Data/student_average_ranks_realmarket.json", "r")
student_av_rank = ast.literal_eval(b_file.read())
b_file.close()

d_file = open("D:/Documents/CDO/CDO_project/Data/school_average_ranks_realmarket.json", "r")
school_av_rank = ast.literal_eval(d_file.read())
d_file.close()

student_sample_ranks = {k: student_av_rank[k] for k in student_av_rank.keys() & {'10', '15', '20', '25', '30', '35', '39'}}
school_sample_ranks = {k: school_av_rank[k] for k in school_av_rank.keys() & {'10', '15', '20', '25', '30', '35', '39'}}


barWidth = 0.25

lists2 = sorted(student_sample_ranks.items()) 
lists3 = sorted(school_sample_ranks.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)

br2 = np.arange(len(x2))
br3 = [x + barWidth for x in br2]

plt.figure(8)
plt.bar(br2, y2, color = 'royalblue', label="Students' average rank", width=barWidth)
plt.bar(br3, y3, color = 'sandybrown', label="Schools' average rank", width=barWidth)
plt.xlabel("Lenght of student's sampled sub-list")
plt.ylabel("Average Rank of stable partner")
plt.xticks([r + barWidth*.5 for r in range(len(x2))], ['10', '15', '20', '25', '30', '35', '40'])
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/ranks_sample_same_list_origin_realmarket.png')
'''


'''
student_Match, school_Match, student_ranks, school_ranks, student_original_preferences, school_original_preferences = nyc.simulation_matching_increase_preferences(1, 10, 1000, 1001, 10)

a_file = open("D:/Documents/CDO/CDO_project/Data/student_Match.json", "w")
json.dump(student_Match, a_file)
a_file.close()

b_file = open("D:/Documents/CDO/CDO_project/Data/school_Match.json", "w")
json.dump(school_Match, b_file)
b_file.close()

c_file = open("D:/Documents/CDO/CDO_project/Data/student_original_pref.json", "w")
json.dump(student_original_preferences, c_file)
c_file.close()

d_file = open("D:/Documents/CDO/CDO_project/Data/school_original_pref.json", "w")
json.dump(school_original_preferences, d_file)
d_file.close()

e_file = open("D:/Documents/CDO/CDO_project/Data/student_ranks_samples.json", "w")
json.dump(student_ranks, e_file)
e_file.close()

f_file = open("D:/Documents/CDO/CDO_project/Data/school_ranks_samples.json", "w")
json.dump(school_ranks, f_file)
f_file.close()

###################################################################

a_file = open("D:/Documents/CDO/CDO_project/Data/student_Match.json", "r")
student_Match = json.loads(a_file.read())
a_file.close()

b_file = open("D:/Documents/CDO/CDO_project/Data/school_Match.json", "r")
school_Match = json.loads(b_file.read())
b_file.close()

c_file = open("D:/Documents/CDO/CDO_project/Data/student_original_pref.json", "r")
student_original_preferences = json.loads(c_file.read())
c_file.close()

d_file = open("D:/Documents/CDO/CDO_project/Data/school_original_pref.json", "r")
school_original_preferences = json.loads(d_file.read())
d_file.close()
'''

'''
################################################################################
# Edges that are in the new match but were not in the previous match
# Complete list of preferences, additions are sampled from the complete list without replacement
################################################################################

student_Match, school_Match, student_ranks, school_ranks, student_original_preferences, school_original_preferences = nyc.simulation_matching_increase_preferences(1, 10, 1000, 1001, 990)

student_changes, school_changes = nyc.differences_match(1, 10, 990, student_Match, school_Match)
total_change_match_students, total_change_match_schools, mean_change_match_students, mean_change_match_schools, num_students_change, num_schools_change = nyc.total_differences_match(student_changes, school_changes)

#student_original_ranks, school_original_ranks = nyc.original_rank(student_Match, school_Match, student_original_preferences, school_original_preferences)    
#student_changes_orank, school_changes_orank = nyc.differences_match(1, 10, 990, student_original_ranks, school_original_ranks)
#total_change_orank_students, total_change_orank_schools, mean_change_orank_students, mean_change_orank_schools, num_students_change_orank, num_schools_change_orank = nyc.total_differences_match(student_changes_orank, school_changes_orank)

barWidth = 0.25

##
lists2 = sorted(total_change_match_students.items()) 
lists3 = sorted(total_change_match_schools.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)
br2 = np.arange(len(x2))
br3 = [x + barWidth for x in br2]
plt.figure(9)
plt.bar(br2, y2, color = 'royalblue', label="Students", width=barWidth)
plt.bar(br3, y3, color = 'sandybrown', label="Schools", width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("|M_k/M_{k-1}|")
plt.xticks([r + barWidth*.5 for r in range(len(x2))], x2, rotation = 90, fontsize = 4)
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/change_match.png')

##
lists2 = sorted(mean_change_match_students.items()) 
lists3 = sorted(mean_change_match_schools.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)
br2 = np.arange(len(x2))
br3 = [x + barWidth for x in br2]
plt.figure(10)
plt.bar(br2, y2, color = 'royalblue', label="Students", width=barWidth)
plt.bar(br3, y3, color = 'sandybrown', label="Schools", width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("mean(M_k/M_{k-1})")
plt.xticks([r + barWidth*.5 for r in range(len(x2))], x2, rotation = 90, fontsize = 4)
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/mean_change_match.png')

###################################################################################################################

lists2 = sorted(num_students_change.items()) 
x2, y2 = zip(*lists2)
br2 = np.arange(len(x2))
plt.figure(12)
plt.bar(br2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("M_k/M_{k-1}")
#plt.xticks([r for r in range(len(x2))], x2, rotation = 90, fontsize = 4)
#plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/edges_change_match_long.png')

student_sample_edges_change = {k: num_students_change[k] for k in num_students_change.keys() & [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

lists2 = sorted(student_sample_edges_change.items()) 
x2, y2 = zip(*lists2)
br2 = np.arange(len(x2))
plt.figure(13)
plt.bar(br2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("M_k/M_{k-1}")
plt.xticks([r for r in range(len(x2))], ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])
#plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/edges_change_match.png')

################################################################################################################################

lists2 = sorted(mean_change_orank_students.items()) 
lists3 = sorted(mean_change_orank_schools.items())
x2, y2 = zip(*lists2)
x3, y3 = zip(*lists3)

br2 = np.arange(len(x2))
br3 = [x + barWidth for x in br2]

plt.figure(14)
plt.bar(br2, y2, color = 'royalblue', label="Students", width=barWidth)
plt.bar(br3, y3, color = 'sandybrown', label="Schools", width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("mean(Rank_k/Rank_{k-1})")
plt.xticks([r + barWidth*.5 for r in range(len(x2))], x2, rotation = 90, fontsize = 4)
plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/change_original_rank.png')
'''


'''
################################################################################
# Simulations of improvement of match when increasing sublist size and of number of
# students that go from being unmatched to being matched
# Complete list of preferences, additions are sampled from the complete list
################################################################################

Delta = 2
k = 10 
additions = 495

student_Match, school_Match, student_ranks, school_ranks, student_original_preferences, school_original_preferences = nyc.simulation_matching_increase_preferences(Delta, k, 1000, 1001, additions)

student_changes, school_changes = nyc.differences_match(Delta, k, additions, student_Match, school_Match)
num_students_change, num_schools_change = nyc.total_differences_match(student_changes, school_changes)

student_unmatched_matched, school_unmatched_matched = nyc.unmatched_matched(Delta, k, additions, student_Match, school_Match)
num_students_unm_mat, num_schools_unm_mat = nyc.total_unmatched_matched(student_unmatched_matched, school_unmatched_matched)

student_original_ranks, school_original_ranks = nyc.original_rank(student_Match, school_Match, student_original_preferences, school_original_preferences)    
student_changes_orank, school_changes_orank = nyc.change_original_rank(Delta, k, additions, student_original_ranks, school_original_ranks)
num_students_imp, num_schools_imp = nyc.improve_original_rank(student_changes_orank, school_changes_orank, num_students_change, num_schools_change)


barWidth = 0.25

lists2 = sorted(num_students_change.items()) 
x2, y2 = zip(*lists2)
br2 = np.arange(len(x2))
plt.figure(15)
plt.bar(br2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("M_k/M_{k-1}")
#plt.xticks([r for r in range(len(x2))], x2, rotation = 90, fontsize = 4)
#plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/edges_change_match_long.png')


student_sample_edges_change = {k: num_students_change[k] for k in num_students_change.keys() & [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}

lists2 = sorted(student_sample_edges_change.items()) 
x2, y2 = zip(*lists2)
br2 = np.arange(len(x2))
plt.figure(16)
plt.bar(br2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("M_k/M_{k-1}")
plt.xticks([r for r in range(len(x2))], ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])
#plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/edges_change_match.png')


lists2 = sorted(num_students_unm_mat.items()) 
x2, y2 = zip(*lists2)
br2 = np.arange(len(x2))
plt.figure(17)
plt.bar(br2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("|Unmatched to Matched|")
#plt.xticks([r for r in range(len(x2))], x2, rotation = 90, fontsize = 4)
#plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/unmatched_to_matched_long.png')


student_sample_edges_change = {k: num_students_unm_mat[k] for k in num_students_unm_mat.keys() & [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}
lists2 = sorted(student_sample_edges_change.items()) 
x2, y2 = zip(*lists2)
br2 = np.arange(len(x2))
plt.figure(18)
plt.bar(br2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("|Unmatched to Matched|")
plt.xticks([r for r in range(len(x2))], ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])
#plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/unmatched_to_matched.png')


lists2 = sorted(num_students_imp.items()) 
x2, y2 = zip(*lists2)
br2 = np.arange(len(x2))
plt.figure(19)
plt.bar(br2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("% Students with better match")
#plt.xticks([r for r in range(len(x2))], x2, rotation = 90, fontsize = 4)
#plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/improvement_rank_match_long.png')


student_sample_imp = {k: num_students_imp[k] for k in num_students_imp.keys() & [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}
lists2 = sorted(student_sample_imp.items()) 
x2, y2 = zip(*lists2)
br2 = np.arange(len(x2))
plt.figure(20)
plt.bar(br2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("% Students with better match")
plt.xticks([r for r in range(len(x2))], ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])
#plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/improvement_rank_match.png')
'''
'''
################################################################################
# MC simulations of improvement of match when increasing sublist size
# Complete list of preferences, additions are sampled from the complete list
################################################################################

#average_students_change, average_students_imp  = nyc.mc_simulations_improvement(10, 10, 99, 1000, 1001, 10)
#print('mean number of students that change match')
#print(average_students_change)
#print('mean pct of students that improve match')
#print(average_students_imp)


average_students_change = {20: 708.9, 30: 604.3, 40: 530.9, 50: 496.40000000000003, 60: 468.1, 70: 443.70000000000005, 80: 423.40000000000003, 90: 396.6, 100: 395.09999999999997, 110: 377.99999999999994, 120: 351.30000000000007, 130: 350.09999999999997, 140: 332.3, 150: 317.40000000000003, 160: 319.5, 170: 325.3, 180: 289.4, 190: 293.59999999999997, 200: 316.6, 210: 291.29999999999995, 220: 281.40000000000003, 230: 275.59999999999997, 240: 280.40000000000003, 250: 261.3, 260: 267.8, 270: 254.7, 280: 243.20000000000002, 290: 249.50000000000003, 300: 255.10000000000002, 310: 258.1, 320: 251.00000000000003, 330: 215.2, 340: 217.2, 350: 225.20000000000002, 360: 214.49999999999997, 370: 208.39999999999998, 380: 222.1, 390: 218.4, 400: 222.50000000000003, 410: 212.9, 420: 199.0, 430: 215.5, 440: 229.0, 450: 180.10000000000002, 460: 210.39999999999998, 470: 215.00000000000006, 480: 180.8, 490: 165.3, 500: 188.4, 510: 192.99999999999997, 520: 202.5, 530: 199.60000000000002, 540: 200.6, 550: 188.6, 560: 200.09999999999997, 570: 211.1, 580: 172.5, 590: 190.4, 600: 197.2, 610: 192.2, 620: 169.39999999999998, 630: 176.29999999999998, 640: 174.7, 650: 187.00000000000003, 660: 183.1, 670: 167.4, 680: 171.29999999999998, 690: 154.4, 700: 180.7, 710: 166.70000000000002, 720: 181.50000000000003, 730: 154.5, 740: 160.0, 750: 144.5, 760: 132.1, 770: 174.39999999999995, 780: 154.89999999999998, 790: 151.10000000000002, 800: 172.6, 810: 156.2, 820: 146.4, 830: 170.5, 840: 140.60000000000002, 850: 150.79999999999998, 860: 150.39999999999998, 870: 173.6, 880: 185.7, 890: 138.1, 900: 157.20000000000002, 910: 141.20000000000002, 920: 155.9, 930: 144.20000000000002, 940: 160.59999999999997, 950: 143.5, 960: 170.4, 970: 165.6, 980: 150.3, 990: 132.4, 1000: 145.79999999999998}
average_students_imp = {20: 0.6603437697856265, 30: 0.6500462220677187, 40: 0.622501604449434, 50: 0.646011828552363, 60: 0.6366042353307886, 70: 0.6579169785023192, 80: 0.588692079902284, 90: 0.592191126201367, 100: 0.6545928726311152, 110: 0.6054538486805756, 120: 0.4804211244980393, 130: 0.6965981554764094, 140: 0.5703615890066691, 150: 0.5285835597541444, 160: 0.5088929697022808, 170: 0.7220961393143404, 180: 0.48897413969898673, 190: 0.49949181221093075, 200: 0.5837441841934747, 210: 0.5493810171038281, 220: 0.5842040276166918, 230: 0.5861277795113052, 240: 0.6065824645342499, 250: 0.5280740805061256, 260: 0.4990878084495688, 270: 0.5199904592370109, 280: 0.5463050257381228, 290: 0.5770601965964348, 300: 0.5715263510480366, 310: 0.5702911708698777, 320: 0.6060856533070155, 330: 0.6320222922629172, 340: 0.4659501206550786, 350: 0.6129259715759644, 360: 0.512170001566213, 370: 0.5997099482287971, 380: 0.4836978548660372, 390: 0.4699111440190411, 400: 0.6171531141600719, 410: 0.5153444228743669, 420: 0.5005085818320142, 430: 0.5207149150203935, 440: 0.5014855290365987, 450: 0.618168644505762, 460: 0.6348833568458673, 470: 0.5398720814688203, 480: 0.4442145025928374, 490: 0.5413247641781801, 500: 0.665217260250599, 510: 0.44620991965333645, 520: 0.648150778039481, 530: 0.37490416081903155, 540: 0.5810231791716068, 550: 0.5296960907388331, 560: 0.5497178570346735, 570: 0.4650649259582978, 580: 0.4897353498939618, 590: 0.4364877861998731, 600: 0.5923008862667697, 610: 0.6428633164286005, 620: 0.5702719407197516, 630: 0.4410076091191854, 640: 0.6003216989685636, 650: 0.5949881003009123, 660: 0.5876693249304321, 670: 0.5164622046349958, 680: 0.49585890847017894, 690: 0.48817040731178063, 700: 0.5065107849723159, 710: 0.524974822006657, 720: 0.6035572748210363, 730: 0.46352782380170765, 740: 0.6134872333319348, 750: 0.48239911473197306, 760: 0.6255254557126207, 770: 0.43165861415650436, 780: 0.5414615312978118, 790: 0.46408408477714974, 800: 0.5806870185309028, 810: 0.45884212484178827, 820: 0.5500579731788781, 830: 0.5948821179920136, 840: 0.5170720668136497, 850: 0.48992737998621744, 860: 0.5133440609555364, 870: 0.5428088925296115, 880: 0.5607992496050251, 890: 0.5869438441539653, 900: 0.3242360475590063, 910: 0.5418915561396659, 920: 0.6598740440080224, 930: 0.522130060736135, 940: 0.637722529646197, 950: 0.576864544216897, 960: 0.4173473522944097, 970: 0.5405797798878653, 980: 0.3979881890012047, 990: 0.49307870521666397, 1000: 0.5027491538651586}
average_number_students_imp = {k: average_students_change[k]*average_students_imp[k] for k in average_students_change.keys()}

barWidth = 2

lists2 = sorted(average_students_change.items()) 
x2, y2 = zip(*lists2)
plt.figure(21)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("M_k/M_{k-1}")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/average_edges_change_match_long10.png')

lists2 = sorted(average_students_imp.items()) 
x2, y2 = zip(*lists2)
plt.figure(22)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("% Students with better match")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/average_improvement_rank_match_long10.png')

lists2 = sorted(average_number_students_imp.items()) 
x2, y2 = zip(*lists2)
plt.figure(23)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("|Students with better match|")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/average_number_improvement_match_long10.png')
'''
'''
#############################################################################################
## Time tests for optimization
#############################################################################################
np.set_printoptions(threshold=sys.maxsize)

start_time = time.time()

student_f_pref, school_f_pref = onyc.marriage_market_preference_lists(1000, 1001)

#print(student_f_pref)
#print(school_f_pref)

print("Original Market --- %s seconds ---" % (time.time() - start_time))

k=10
additions = 900
Delta = 1
student_pre = {}
school_pre = {}
student_M = {}
school_M = {}

student_pre[k], school_pre[k] = onyc.restricted_market(k, student_f_pref, school_f_pref)
#print(student_pre)
#print(school_pre)
print("Restricted Market --- %s seconds ---" % (time.time() - start_time))

student_M[k], school_M[k] = onyc.gale_shapley_modified(1000, 1001, student_pre[k], school_pre[k])
print("GS --- %s seconds ---" % (time.time() - start_time))


for j in range(1,additions+1):
    k_prev = k
    k = k + Delta
    print('working on sublist size: ' + str(k))
    student_pre[k], school_pre[k] = onyc.increase_preference_sublist(Delta, student_pre[k_prev], school_pre[k_prev], student_f_pref, school_f_pref)
    print("Increase --- %s seconds ---" % (time.time() - start_time))
    student_M[k], school_M[k] = onyc.gale_shapley_modified(1000, 1001, student_pre[k], school_pre[k])
    print("GS --- %s seconds ---" % (time.time() - start_time))
'''

################################################################################
# MC simulations of improvement of match when increasing sublist size
# Complete list of preferences, additions are sampled from the complete list
################################################################################

average_students_change, average_schools_change, average_students_unm_mat, average_schools_unm_mat, average_students_imp, average_schools_imp, average_nash_welfare  = onyc.mc_simulations_improvement(1, 10, 990, 1000, 1001, 5)

barWidth = 0.25

average_nash_welfare = {10: 6189.166703970055, 11: 6254.3614531603125, 12: 6295.042509969029, 13: 6358.920188185219, 14: 6374.863955703841, 15: 6388.879383534898, 16: 6411.329678657702, 17: 6439.501058461033, 18: 6456.830618741786, 19: 6482.810519157436, 20: 6497.464754370879, 21: 6506.767224905683, 22: 6520.791178777066, 23: 6539.680333009964, 24: 6558.965754939951, 25: 6562.239199142805, 26: 6586.892737463199, 27: 6604.522037591315, 28: 6608.8143100680045, 29: 6627.445957804166, 30: 6627.363610220862, 31: 6638.3838172273645, 32: 6634.829276456148, 33: 6650.64176281399, 34: 6644.750539549473, 35: 6669.945369034183, 36: 6658.577363653383, 37: 6672.178699328291, 38: 6683.415654200626, 39: 6694.935194494175, 40: 6693.4344541079845, 41: 6687.962140648055, 42: 6700.549673537797, 43: 6710.485218180734, 44: 6709.357788831925, 45: 6708.533740644412, 46: 6717.090483877583, 47: 6726.3357844125585, 48: 6730.3783136422635, 49: 6727.836931903361, 50: 6731.9032482916755, 51: 6736.493213275399, 52: 6742.208072597919, 53: 6740.633849863195, 54: 6739.0250759133, 55: 6752.682851124555, 56: 6752.307239178781, 57: 6756.744891514227, 58: 6759.133253962609, 59: 6753.4186783066725, 60: 6755.128421455686, 61: 6760.016068011119, 62: 6764.910590660207, 63: 6763.876300419894, 64: 6764.340173125667, 65: 6769.2371593862335, 66: 6773.352687092121, 67: 6776.394877229402, 68: 6773.092716563415, 69: 6781.178361695416, 70: 6783.257853804274, 71: 6775.245712289503, 72: 6782.798358831303, 73: 6792.412177236814, 74: 6783.1246456071085, 75: 6786.506784473122, 76: 6787.836021614355, 77: 6791.995433324175, 78: 6796.816551689535, 79: 6797.598107216602, 80: 6796.491128283949, 81: 6792.157845616241, 82: 6790.528613109007, 83: 6800.506954765855, 84: 6803.437745791973, 85: 6801.531054442877, 86: 6804.360603288678, 87: 6811.93505293567, 88: 6807.651346429375, 89: 6813.9558305221, 90: 6812.687353336367, 91: 6806.358759951241, 92: 6811.918229882236, 93: 6810.298592031641, 94: 6810.753584481197, 95: 6812.140230037735, 96: 6815.476338847948, 97: 6817.504158776452, 98: 6819.691691950491, 99: 6813.603581878469, 100: 6810.05513372779, 101: 6812.203584947289, 102: 6819.120719414319, 103: 6825.805364066353, 104: 6818.004411629468, 105: 6818.954606301057, 106: 6820.514798465654, 107: 6817.271558231572, 108: 6826.291578830014, 109: 6828.351951666634, 110: 6824.21114249753, 111: 6827.323802504296, 112: 6829.413001746576, 113: 6831.231094032987, 114: 6827.817337999921, 115: 6828.620041991291, 116: 6824.555897870256, 117: 6831.9219720757665, 118: 6830.434703632538, 119: 6829.389201125952, 120: 6830.555815243618, 121: 6832.86614290922, 122: 6836.079381287992, 123: 6837.639238935863, 124: 6837.868812120096, 125: 6835.289371947944, 126: 6834.24454348411, 127: 6832.1101899164805, 128: 6832.116574015356, 129: 6835.643088463654, 130: 6834.129025197773, 131: 6838.712928553374, 132: 6840.612797509077, 133: 6837.431212850339, 134: 6835.9469015611985, 135: 6839.72798212412, 136: 6842.247192589325, 137: 6844.00517502213, 138: 6849.045878954872, 139: 6847.823901615122, 140: 6841.796711092385, 141: 6841.593744632091, 142: 6845.9843386891835, 143: 6840.358650000222, 144: 6845.711786357273, 145: 6843.137212171874, 146: 6845.160536871685, 147: 6848.7934042660845, 148: 6852.834735946684, 149: 6855.1252640715065, 150: 6849.052844597991, 151: 6847.956729696263, 152: 6848.400200187633, 153: 6848.934882711103, 154: 6851.369709654889, 155: 6850.238555503587, 156: 6851.655118465106, 157: 6852.008698062524, 158: 6852.883270233805, 159: 6852.215601662243, 160: 6852.638369593292, 161: 6851.856994402868, 162: 6855.9676853575065, 163: 6854.077316558167, 164: 6856.7179811578535, 165: 6855.026087605733, 166: 6855.089712993681, 167: 6852.530251739104, 168: 6857.5463574451205, 169: 6856.199297055063, 170: 6852.257443036477, 171: 6855.631604322112, 172: 6854.577922250244, 173: 6851.4538111021175, 174: 6851.653887576547, 175: 6849.931504883713, 176: 6854.475685770085, 177: 6857.586312953639, 178: 6852.815483386468, 179: 6857.093276643176, 180: 6853.851290843044, 181: 6853.07642840622, 182: 6853.8695767746085, 183: 6854.519426600208, 184: 6853.660115067538, 185: 6857.5848326571395, 186: 6860.5417970651215, 187: 6858.7665102584, 188: 6858.977058802452, 189: 6858.476498245263, 190: 6858.465969456841, 191: 6861.289778227703, 192: 6861.356346743939, 193: 6860.176069325068, 194: 6860.048532800401, 195: 6860.170441558488, 196: 6861.027400893709, 197: 6863.39191320604, 198: 6860.3943576083, 199: 6864.6405451457995, 200: 6866.6978099604985, 201: 6863.344312100135, 202: 6863.637145047225, 203: 6862.181664334621, 204: 6864.450476534426, 205: 6863.884122330013, 206: 6865.009013016325, 207: 6863.942444794493, 208: 6864.785585687121, 209: 6862.82504371989, 210: 6864.912006085224, 211: 6864.585778865191, 212: 6862.682525881022, 213: 6869.074938211934, 214: 6867.4154392921955, 215: 6865.086483308656, 216: 6865.4219501937605, 217: 6862.9359762941485, 218: 6864.283870287953, 219: 6868.314871413372, 220: 6866.980827951589, 221: 6868.286841974936, 222: 6868.82180937733, 223: 6871.815632470262, 224: 6865.999883708275, 225: 6869.50978355682, 226: 6870.713673973386, 227: 6871.562433437879, 228: 6869.722340147989, 229: 6871.521686141956, 230: 6870.15111914151, 231: 6868.638324167872, 232: 6865.618069022182, 233: 6869.417343464745, 234: 6869.782492398215, 235: 6870.48066617801, 236: 6869.731021133425, 237: 6871.413672197152, 238: 6869.4428837790965, 239: 6869.593422258166, 240: 6873.560894919458, 241: 6869.634768069772, 242: 6869.972509390657, 243: 6871.1903695594965, 244: 6870.424982131836, 245: 6871.449581603405, 246: 6871.208611094434, 247: 6869.874328590111, 248: 6871.736607719109, 249: 6874.47212783392, 250: 6870.625415958127, 251: 6875.640418292029, 252: 6872.416830409, 253: 6872.732044034288, 254: 6873.361395095862, 255: 6873.957333315511, 256: 6874.789896777098, 257: 6875.719071972448, 258: 6875.317254333989, 259: 6875.6699639321505, 260: 6878.1993886247055, 261: 6875.906085801464, 262: 6875.839914901639, 263: 6881.996243389503, 264: 6873.467245745466, 265: 6872.505483067518, 266: 6877.514446416641, 267: 6875.510067979352, 268: 6874.512177453975, 269: 6877.97993023193, 270: 6881.478507518603, 271: 6880.343466086091, 272: 6878.5436789263185, 273: 6876.42267970213, 274: 6874.018612435488, 275: 6876.233683764252, 276: 6873.0705815049305, 277: 6877.921778609807, 278: 6877.3131005341365, 279: 6875.460774348012, 280: 6873.43470903407, 281: 6872.853635291145, 282: 6870.364382663472, 283: 6873.254166854818, 284: 6877.184710347718, 285: 6876.374485943827, 286: 6876.7625688963035, 287: 6879.412276155632, 288: 6879.071998897006, 289: 6879.571116115685, 290: 6877.594686536429, 291: 6876.407347317074, 292: 6879.765573679586, 293: 6877.748877250614, 294: 6879.630521987787, 295: 6878.021429090131, 296: 6878.57456276411, 297: 6879.448210319504, 298: 6877.176225919038, 299: 6876.113585008485, 300: 6879.212233728602, 301: 6878.355692587336, 302: 6877.724028384506, 303: 6875.725146849101, 304: 6877.890763940038, 305: 6878.422503616408, 306: 6873.6478425156965, 307: 6875.475821139072, 308: 6878.381347477463, 309: 6877.212884416627, 310: 6877.82168132529, 311: 6878.1653188226055, 312: 6879.155585774175, 313: 6880.02728808349, 314: 6880.448783863083, 315: 6879.737683993611, 316: 6880.820800063965, 317: 6876.476065495258, 318: 6880.221095999716, 319: 6883.192051563123, 320: 6881.068924265342, 321: 6882.248287524879, 322: 6883.3638847175025, 323: 6884.117438084495, 324: 6883.881790519827, 325: 6884.4342165040525, 326: 6885.219433021633, 327: 6882.308291512528, 328: 6881.748445567957, 329: 6879.681635730985, 330: 6880.5325317423985, 331: 6879.97868703902, 332: 6883.5197826584135, 333: 6882.20014179319, 334: 6883.1771065405155, 335: 6882.344040139805, 336: 6886.426855241815, 337: 6883.259226885853, 338: 6887.177347954878, 339: 6886.8666130451875, 340: 6884.137584092796, 341: 6887.30623304003, 342: 6886.603102564821, 343: 6887.490274503679, 344: 6883.157247620709, 345: 6883.302234592588, 346: 6885.098769338676, 347: 6883.481261505425, 348: 6881.860938892734, 349: 6880.717807178617, 350: 6883.235564457647, 351: 6884.22692430419, 352: 6884.434731024924, 353: 6886.197096575519, 354: 6886.050582098449, 355: 6888.268159274527, 356: 6886.0264188132405, 357: 6883.3316697764485, 358: 6885.13308863312, 359: 6887.507921439776, 360: 6886.8389487533095, 361: 6884.825909922372, 362: 6885.379426423438, 363: 6884.515982912639, 364: 6884.90189464486, 365: 6883.351563150761, 366: 6886.3320674245515, 367: 6884.692176611334, 368: 6883.471019116981, 369: 6882.0747567193175, 370: 6888.62678330471, 371: 6888.939291048552, 372: 6892.428371888667, 373: 6891.9377295706145, 374: 6890.848260265788, 375: 6888.176746879981, 376: 6887.515387147923, 377: 6889.286465719706, 378: 6891.260619757467, 379: 6887.020251571135, 380: 6887.426717865659, 381: 6888.402106415275, 382: 6888.68595752116, 383: 6887.613274198113, 384: 6889.0861880733755, 385: 6888.426419382202, 386: 6887.925317685349, 387: 6885.933038942832, 388: 6885.107828153026, 389: 6887.152600594134, 390: 6890.572372111685, 391: 6886.734319755296, 392: 6888.779887240997, 393: 6889.3204157440905, 394: 6887.407528357784, 395: 6890.998569841398, 396: 6886.7468391878565, 397: 6886.071769300909, 398: 6884.6237504460505, 399: 6888.384142444533, 400: 6888.533476394386, 401: 6889.860531523624, 402: 6889.345399185006, 403: 6887.099372515577, 404: 6889.111072811453, 405: 6888.390661023083, 406: 6888.254981641925, 407: 6888.810557231445, 408: 6889.474713002455, 409: 6888.966438177122, 410: 6888.538086459776, 411: 6889.614398984735, 412: 6889.208542603212, 413: 6889.6923777952325, 414: 6888.869204198072, 415: 6888.656762955646, 416: 6888.789178235703, 417: 6887.053069168865, 418: 6887.535702752133, 419: 6891.02197982305, 420: 6889.0921117817725, 421: 6890.40223875071, 422: 6890.201860418223, 423: 6891.13878705338, 424: 6891.512812127723, 425: 6890.222430266469, 426: 6889.206145523736, 427: 6890.701048666744, 
428: 6890.787652740704, 429: 6892.608305399992, 430: 6891.06696873838, 431: 6891.405175401533, 432: 6891.643691032215, 433: 6895.8838818790455, 434: 6893.87103715364, 435: 6894.446680588392, 436: 6892.94127407486, 437: 6894.318151118905, 438: 6891.9610408706285, 439: 6894.064123092973, 440: 6893.199293475329, 441: 6894.124175611745, 442: 6891.7390320012655, 443: 6893.851638478563, 444: 6894.392533056827, 445: 6893.333805864368, 446: 6891.67218482426, 447: 6893.5612568441575, 448: 6891.882419557109, 449: 6891.384399608148, 450: 6889.99085151905, 451: 6890.739999961223, 452: 6891.674265944128, 453: 6890.8150741216605, 454: 6894.643154499143, 455: 6892.088700889115, 456: 6891.980100188336, 457: 6891.5593323858075, 458: 6891.055067544099, 459: 6891.9002755028305, 460: 6888.192891700608, 461: 6890.677536275655, 462: 6891.867419507866, 463: 6892.163510153631, 464: 6892.328350610137, 465: 6891.164159133675, 466: 6891.541477012678, 467: 6890.923388917776, 468: 6893.394973491204, 469: 6896.390947909666, 470: 6894.471643621389, 471: 6893.817643795118, 472: 6892.616596177169, 473: 6892.012647484964, 474: 6893.933212461752, 475: 6894.208758590701, 476: 6893.793003418604, 477: 6895.239940142568, 478: 6893.958854748367, 479: 6893.163396857599, 480: 6894.11775691882, 481: 6893.464412992123, 482: 6892.667900769037, 483: 6894.20039710916, 484: 6891.260830835605, 485: 6893.217384637139, 486: 6893.7772655576955, 487: 6891.007498366607, 488: 6891.926385847387, 489: 6891.236175107703, 490: 6892.524119498328, 491: 6892.627061649682, 492: 6893.141785928607, 493: 6893.8101089515285, 494: 6893.952935659505, 495: 6894.28857102638, 496: 6891.264301444304, 497: 6890.839190538245, 498: 6892.832943123036, 499: 6894.132794105571, 500: 6893.008618345666, 501: 6894.149560379265, 502: 6894.097398291986, 503: 6892.688235128588, 504: 6893.170497547203, 505: 6893.263448157673, 506: 6892.291932300015, 507: 6892.140247344139, 508: 6892.627157625295, 509: 6895.037346479027, 510: 6893.595956563442, 511: 6894.495758101339, 512: 6894.60100460626, 513: 6893.125875745808, 514: 6894.06879979238, 515: 6891.670605781643, 516: 6893.155743509623, 517: 6896.73460475926, 518: 6892.886151276955, 519: 6892.922365998813, 520: 6892.9094859864845, 521: 6893.295888443857, 522: 6893.735842429651, 523: 6892.563331304494, 524: 6894.000890885558, 525: 6893.56234425163, 526: 6895.3744137217445, 527: 6895.570046698154, 528: 6895.712240844152, 529: 6896.121743197666, 530: 6895.419696891395, 531: 6893.985463501692, 532: 6895.295558048121, 533: 6892.1618924566865, 534: 6894.294984306, 535: 6894.779342450016, 536: 6895.22386871246, 537: 6894.702552866541, 538: 6894.892596227425, 539: 6894.754259523084, 540: 6895.5711907755995, 541: 6894.118782433146, 542: 6894.05138671151, 543: 6893.702432514362, 544: 6892.984039841747, 545: 6895.933022717783, 546: 6892.2183270479145, 547: 6891.9192709000945, 548: 6893.17898723646, 549: 6893.012645023739, 550: 6895.328267646351, 551: 6895.963137655997, 552: 6895.559038590907, 553: 6895.059410830854, 554: 6895.262073193679, 555: 6895.646487096985, 556: 6896.6020531795375, 557: 6896.388303867263, 558: 6896.723143055584, 559: 6894.699613289603, 560: 6895.093725185443, 561: 6896.363184382126, 562: 6896.372164657723, 563: 6895.892843815767, 564: 6897.771307460585, 565: 6896.755834112877, 566: 6896.67434542377, 567: 6896.905734640495, 568: 6895.513899625737, 569: 6896.17718273634, 570: 6898.288979700926, 571: 6898.810638364195, 572: 6897.498473703238, 573: 6897.769463993995, 574: 6896.973975028668, 575: 6895.354054944778, 576: 6896.453123811965, 577: 6896.6270793713065, 578: 6896.492193835844, 579: 6897.697205861421, 580: 6897.634269911757, 581: 6896.531957797879, 582: 6897.629421355594, 583: 6897.916966589262, 584: 6897.923578016345, 585: 6898.805182491405, 586: 6897.828110175433, 587: 6897.859437805009, 588: 6897.22827112506, 589: 6897.462301919413, 590: 6898.807298207505, 591: 6896.6973911614205, 592: 6895.4364222225195, 593: 6897.424366412542, 594: 6897.198430791688, 595: 6897.329324638258, 596: 6895.60418228525, 597: 6897.783904983835, 598: 6896.477282327807, 599: 6896.752127107069, 600: 6894.73460053003, 601: 6896.642418043203, 602: 6897.168371873813, 603: 6897.28555641257, 604: 6895.735603018176, 605: 6893.407742424264, 606: 6895.029558285558, 607: 6896.8168903206915, 608: 6897.696249871315, 609: 6897.25922006301, 610: 6897.061048705635, 611: 6896.019134119026, 612: 6895.269357847072, 613: 6896.197496920224, 614: 6896.680546467882, 615: 6896.478431118267, 616: 6898.311061475781, 617: 6897.2698487379075, 618: 6895.595074626788, 619: 6897.659569631598, 620: 6897.7048015762175, 621: 6896.15401054104, 622: 6897.364586762747, 623: 6897.58331340053, 624: 6898.669825730426, 625: 6898.507198493022, 626: 6898.06736001454, 627: 6898.400954448934, 628: 6898.617411746736, 629: 6897.715143350239, 630: 6897.984550542275, 631: 6899.458519309846, 632: 6899.133459954333, 633: 6899.208585797735, 634: 6897.272996434892, 635: 6897.522621067452, 636: 6896.3966751823555, 637: 6895.389923082712, 638: 6897.314718883302, 639: 6900.046346618277, 640: 6900.024559001464, 641: 6898.5183750271735, 642: 6898.3362128669305, 643: 6896.766179127744, 644: 6898.012192130177, 645: 6898.030699967461, 646: 6898.50588428124, 647: 6897.501023995696, 648: 6897.779930237982, 649: 6896.534226210819, 650: 6895.95213139885, 651: 6897.663135141411, 652: 6898.987343615415, 653: 6898.667529257287, 654: 6898.619273537533, 655: 6897.964099999268, 656: 6898.869899062229, 657: 6899.360479732706, 658: 6899.511156515662, 659: 6898.948980078304, 660: 6898.897454119257, 661: 6898.931455207683, 662: 6898.784013617413, 663: 6898.47670896651, 664: 6898.97021994213, 665: 6898.925001005406, 666: 6899.372152898887, 667: 6898.223219808365, 668: 6897.08847916282, 669: 6897.824248555156, 670: 6898.280233510957, 671: 6897.810868355071, 672: 6899.670242317105, 673: 6899.023568502542, 674: 6898.952451758462, 675: 6900.408194008582, 676: 6900.147291585678, 677: 6900.03574022252, 678: 6896.374587226297, 679: 6897.008027664559, 680: 6897.140409207395, 681: 6896.471291475395, 682: 6897.64817592241, 683: 6898.022300243161, 684: 6898.360115322763, 685: 6898.631314835844, 686: 6897.255210706274, 687: 6898.5605167877375, 688: 6898.51949834232, 689: 6898.348956395596, 690: 6896.009697255349, 691: 6898.525325794595, 692: 6898.0872211843625, 693: 6897.071516140701, 694: 6898.937266838891, 695: 6898.047726501243, 696: 6900.03022801551, 697: 6900.999886879532, 698: 6900.063285497303, 699: 6899.575223315539, 700: 6898.625070798404, 701: 6898.678106922567, 702: 6897.466998411471, 703: 6897.492187567523, 704: 6899.987794320707, 705: 6899.956050321981, 706: 6899.807532489407, 707: 6899.821980396545, 708: 6899.864852131206, 709: 6899.717547474879, 710: 6899.608439868678, 711: 6899.541225747449, 712: 6900.340700450139, 713: 6898.8826208520995, 714: 6900.404187783416, 715: 6900.239181085202, 716: 6899.455462111988, 717: 6899.877898347548, 718: 6899.995802821977, 719: 6900.319212565972, 720: 6899.8527056551675, 721: 6900.191877889491, 722: 6899.748755055308, 723: 6899.638519218988, 724: 6900.80218050702, 725: 6900.992420791195, 726: 6900.888349434681, 727: 6898.4530391752505, 728: 6899.184861684766, 729: 6900.059294167718, 730: 6900.687694991603, 731: 6901.2703706226675, 732: 6899.4305584097865, 733: 6901.101023458767, 734: 6900.852931418288, 735: 6901.021759871263, 736: 6901.854343327175, 737: 6900.540158342426, 738: 6901.4933093237805, 739: 6901.450734306692, 740: 6901.867675752955, 741: 6901.916017876912, 742: 6899.839777714043, 743: 6899.776626642284, 744: 6899.827706829537, 745: 6901.384381395443, 746: 6900.726546836842, 747: 6901.078195759848, 748: 6900.526573015051, 749: 6899.685552206838, 750: 6900.551438805827, 751: 6900.172577049967, 752: 6900.046399816245, 753: 6900.767496475251, 754: 6900.8469227011465, 755: 6900.821204899947, 756: 6901.11931590535, 757: 6900.692730384706, 758: 6900.494861075373, 759: 6900.774470066982, 760: 6900.747357356581, 761: 6900.689719975095, 762: 6901.040058792747, 763: 6899.914098480412, 764: 6900.7520760621155, 765: 6899.946193770955, 766: 6899.974531935675, 767: 6900.087210481898, 768: 6900.664730785986, 769: 6900.4196762069805, 770: 6900.697617691563, 771: 6900.132512170431, 772: 6899.784387979798, 773: 6901.0577814027, 774: 6901.171742482845, 775: 6901.324673095954, 776: 6901.171092658312, 777: 6901.430287785697, 778: 6900.7187419908905, 779: 6901.309159293745, 780: 6899.565850746656, 781: 6900.431113831204, 782: 6900.595050285299, 783: 6900.159336294414, 784: 6900.256576447667, 785: 6901.639923972176, 786: 6901.5838067334835, 787: 6901.2485718600965, 788: 6901.401122142581, 789: 6901.382388864231, 790: 6901.101856703121, 791: 6901.106810498118, 792: 6901.900144783234, 793: 6901.850914525305, 794: 6901.672096402761, 795: 6901.878667417735, 796: 6901.666542528344, 797: 6901.879684692975, 798: 6901.791984820975, 799: 6901.855946164482, 800: 6901.734557455331, 801: 6901.972262145311, 802: 6901.922139612976, 803: 6901.945671944991, 804: 6901.745808967961, 805: 6902.005325430047, 806: 6900.829041461294, 807: 6901.007678916395, 808: 6901.5058639332165, 809: 6901.437791293032, 810: 6900.971677207176, 811: 6900.681032743178, 812: 6900.42138383633, 813: 6901.011895933005, 814: 6900.980674010625, 815: 6900.888804968696, 816: 6901.176857956729, 817: 6900.501223483116, 818: 6902.132625638954, 819: 6901.524720779786, 820: 6900.84528838245, 821: 6901.223553268099, 822: 6901.743745296361, 823: 6901.9270014344165, 824: 6901.96266239509, 825: 6902.0488685369855, 826: 6901.747612291032, 827: 6901.901571660695, 828: 6901.955487223387, 829: 6901.550589925942, 830: 6901.393795168704, 831: 6901.033447689398, 832: 6901.720893570571, 833: 6902.293554226597, 834: 6902.241064375437, 835: 6901.868873051324, 836: 6901.966809880638, 837: 6901.841142291971, 838: 6901.908951946027, 839: 6902.21498579852, 840: 6902.407009975712, 841: 6902.419098184006, 842: 6902.375901115434, 843: 6902.216206716199, 
844: 6901.807264354642, 845: 6901.925774537196, 846: 6902.040589618259, 847: 6901.871616062848, 848: 6901.595129645371, 849: 6901.809386345686, 850: 6902.157182238826, 851: 6902.021020086485, 852: 6902.189002445608, 853: 6902.292940346168, 854: 6902.338317011127, 855: 6901.837558023916, 856: 6901.455371003488, 857: 6901.65498751707, 858: 6901.928615237924, 859: 6901.835093109548, 860: 6902.337703473642, 861: 6902.409648060532, 862: 6902.358048778178, 863: 6902.475826571266, 864: 6902.108202825371, 865: 6902.421933353386, 866: 6902.0218398671095, 867: 6901.108639197308, 868: 6902.653600789439, 869: 6902.330686356249, 870: 6902.45724753193, 871: 6902.671329306173, 872: 6902.498075008332, 873: 6902.607759962077, 874: 6902.619429162671, 875: 6902.536514722188, 876: 6902.095323140598, 877: 6901.690233666233, 878: 6901.781923340261, 879: 6901.798839902411, 880: 6902.458756767864, 881: 6902.787547986783, 882: 6901.340989595789, 883: 6901.260695182258, 884: 6901.214842613226, 885: 6901.669979554558, 886: 6901.866376407493, 887: 6901.590239492401, 888: 6902.695188624991, 889: 6902.702841861779, 890: 6902.800051795537, 891: 6902.839430006576, 892: 6902.608032524317, 893: 6902.364465362393, 894: 6902.3888289076085, 895: 6902.585569126051, 896: 6902.5590915462235, 897: 6902.501465443498, 898: 6902.467653364249, 899: 6902.614600263785, 900: 6902.830757556369, 901: 6902.371338854264, 902: 6902.71746751805, 903: 6902.915776286718, 904: 6902.669994339476, 905: 6902.180905230481, 906: 6902.846966552688, 907: 6902.581779719605, 908: 6902.205472649527, 909: 6902.491058862181, 910: 6902.413588884274, 911: 6902.358539729619, 912: 6902.857477203188, 913: 6902.722464616609, 914: 6902.65074375809, 915: 6902.714539971827, 916: 6902.76722220368, 917: 6902.865514402212, 918: 6902.940653205658, 919: 6902.938479955095, 920: 6902.843995271136, 921: 6902.767894622113, 922: 6903.256963928604, 923: 6903.388875566691, 924: 6903.286552890307, 925: 6903.2150647852295, 926: 6903.047613854657, 927: 6902.721101376383, 928: 6902.638113031839, 929: 6902.622149071169, 930: 6901.969630462723, 931: 6902.620000489075, 932: 6902.418908370249, 933: 6903.172953821366, 934: 6903.291853625082, 935: 6903.088379318982, 936: 6903.056025626814, 937: 6903.205931745354, 938: 6903.290207911894, 939: 6903.451506645815, 940: 6903.539436756259, 941: 6903.298346707029, 942: 6903.124329361433, 943: 6903.101476477207, 944: 6903.4229071725495, 945: 6903.370021131335, 946: 6903.295573139258, 947: 6903.12555639024, 948: 6903.539518090507, 949: 6903.424616175087, 950: 6903.2921680455365, 951: 6903.473910512372, 952: 6903.5818702913, 953: 6903.501604045117, 954: 6903.616299902004, 955: 6903.062573979734, 956: 6903.545360108979, 957: 6903.181397726757, 958: 6903.266230629036, 959: 6903.185925797471, 960: 6903.1677858284675, 961: 6903.264933112873, 962: 6903.333543217064, 963: 6903.2306324139845, 964: 6903.319682524456, 965: 6903.305765406758, 966: 6903.123325277483, 967: 6902.740932820016, 968: 6902.577073329156, 969: 6902.841739637184, 970: 6902.755309592214, 971: 6903.094649526071, 972: 6903.198013139876, 973: 6903.251753094419, 974: 6903.056767514539, 975: 6903.271627223008, 976: 6902.991483963384, 977: 6902.8795632128, 978: 6902.873852036313, 979: 6902.883749321592, 980: 6902.822215197434, 981: 6902.949534309142, 982: 6902.984551212062, 983: 6903.174142115923, 984: 6903.3864466430305, 985: 6903.563585417849, 986: 6903.392512916255, 987: 6903.597151210054, 988: 6903.392985377412, 989: 6903.171463069291, 990: 6903.350580077531, 991: 6903.0699704994695, 992: 6903.1145150399025, 993: 6902.9701883395155, 994: 6903.190247206932, 995: 6903.6174678082525, 996: 6903.656999200366, 997: 6903.317471963193, 998: 6902.629929519533, 999: 6902.880546803364, 1000: 6902.99626992507}

lists2 = sorted(average_students_change.items()) 
x2, y2 = zip(*lists2)
plt.figure(24)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("M_k/M_{k-1}")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/average_edges_change_match_students.png')

lists2 = sorted(average_students_imp.items()) 
x2, y2 = zip(*lists2)
plt.figure(25)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("% Students with better match")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/average_improvement_rank_match_students.png')

lists2 = sorted(average_students_unm_mat.items()) 
x2, y2 = zip(*lists2)
plt.figure(26)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("|Students unmatched to matched|")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/average_number_students_unm_match.png')

lists2 = sorted(average_schools_change.items()) 
x2, y2 = zip(*lists2)
plt.figure(27)
plt.bar(x2, y2, color = 'sandybrown',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("M_k/M_{k-1} for schools")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/average_edges_change_match_schools.png')

lists2 = sorted(average_schools_imp.items()) 
x2, y2 = zip(*lists2)
plt.figure(28)
plt.bar(x2, y2, color = 'sandybrown',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("% Schools with better match")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/average_improvement_rank_match_schools.png')

lists2 = sorted(average_schools_unm_mat.items()) 
x2, y2 = zip(*lists2)
plt.figure(29)
plt.bar(x2, y2, color = 'sandybrown',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("|Schools unmatched to matched|")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/average_number_schools_unm_match.png')

lists2 = sorted(average_nash_welfare.items()) 
x2, y2 = zip(*lists2)
plt.figure(30)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("Nash Social Welfare")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/average_nash_social_welfare.png')

k_sample = [size for size in range(11,41)]

sample_students_change = {k: average_students_change[k] for k in average_students_change.keys() & k_sample}
sample_students_imp = {k: average_students_imp[k] for k in average_students_imp.keys() & k_sample}
sample_students_unm_mat = {k: average_students_unm_mat[k] for k in average_students_unm_mat.keys() & k_sample}
sample_schools_change = {k: average_schools_change[k] for k in average_schools_change.keys() & k_sample}
sample_schools_imp = {k: average_schools_imp[k] for k in average_schools_imp.keys() & k_sample}
sample_schools_unm_mat = {k: average_schools_unm_mat[k] for k in average_schools_unm_mat.keys() & k_sample}
sample_nash_welfare = {k: average_nash_welfare[k] for k in average_nash_welfare.keys() & k_sample}

lists2 = sorted(sample_students_change.items()) 
x2, y2 = zip(*lists2)
plt.figure(31)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("M_k/M_{k-1}")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/subset_edges_change_match_students.png')

lists2 = sorted(sample_students_imp.items()) 
x2, y2 = zip(*lists2)
plt.figure(32)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("% Students with better match")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/subset_improvement_rank_match_students.png')

lists2 = sorted(sample_students_unm_mat.items()) 
x2, y2 = zip(*lists2)
plt.figure(33)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("|Students unmatched to matched|")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/subset_number_students_unm_match.png')

lists2 = sorted(sample_schools_change.items()) 
x2, y2 = zip(*lists2)
plt.figure(34)
plt.bar(x2, y2, color = 'sandybrown',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("M_k/M_{k-1} for schools")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/subset_edges_change_match_schools.png')

lists2 = sorted(sample_schools_imp.items()) 
x2, y2 = zip(*lists2)
plt.figure(35)
plt.bar(x2, y2, color = 'sandybrown',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("% Schools with better match")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/subset_improvement_rank_match_schools.png')

lists2 = sorted(sample_schools_unm_mat.items()) 
x2, y2 = zip(*lists2)
plt.figure(36)
plt.bar(x2, y2, color = 'sandybrown',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("|Schools unmatched to matched|")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/subset_number_schools_unm_match.png')

lists2 = sorted(sample_nash_welfare.items()) 
x2, y2 = zip(*lists2)
plt.figure(37)
plt.bar(x2, y2, color = 'royalblue',  width=barWidth)
plt.xlabel("Lenght of student's sub-list")
plt.ylabel("Nash Social Welfare")
plt.savefig('D:/Documents/CDO/CDO_project/Figures_opt/subset_nash_social_welfare.png')

print('code succesfull')