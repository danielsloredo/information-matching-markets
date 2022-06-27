from turtle import color
import numpy as np
import unbalanced_matching as um
import counselor_matching as cm
import real_change_on_rank as rc
import nyc_school_market as nyc
import matplotlib.pyplot as plt
import json
import ast
import sys

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
import optim_nyc as onyc
import time
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



print('code succesfull')