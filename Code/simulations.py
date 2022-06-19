from turtle import color
import numpy as np
import unbalanced_matching as um
import counselor_matching as cm
import real_change_on_rank as rc
import nyc_school_market as nyc
import matplotlib.pyplot as plt
import json
import ast

'''
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
lenght_lists = list(range(10,100,1))

student_pre, student_av_rank, school_pre, school_av_rank = nyc.simulationMatchingMarket(1000, 1001, lenght_lists, 10)

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
lenght_lists = list(range(5,40,1))

student_pre, student_av_rank, school_pre, school_av_rank = nyc.simulationMatchingMarket(7500, 7300, lenght_lists, 5)

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
student_Match, school_Match, student_ranks, school_ranks, student_original_preferences, school_original_preferences = nyc.simulationMatchingIncreasePreferences(1, 10, 1000, 1001, 10)

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
student_Match, school_Match, student_ranks, school_ranks, student_original_preferences, school_original_preferences = nyc.simulationMatchingIncreasePreferences(1, 10, 1000, 1001, 990)

student_changes, school_changes = nyc.differencesMatch(1, 10, 990, student_Match, school_Match)
total_change_match_students, total_change_match_schools, mean_change_match_students, mean_change_match_schools, num_students_change, num_schools_change = nyc.totalDifferencesMatch(student_changes, school_changes)

#student_original_ranks, school_original_ranks = nyc.originalRank(student_Match, school_Match, student_original_preferences, school_original_preferences)    
#student_changes_orank, school_changes_orank = nyc.differencesMatch(1, 10, 990, student_original_ranks, school_original_ranks)
#total_change_orank_students, total_change_orank_schools, mean_change_orank_students, mean_change_orank_schools, num_students_change_orank, num_schools_change_orank = nyc.totalDifferencesMatch(student_changes_orank, school_changes_orank)

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




student_Match, school_Match, student_ranks, school_ranks, student_original_preferences, school_original_preferences = nyc.simulationMatchingIncreasePreferences(2, 10, 1000, 1001, 495)

student_changes, school_changes = nyc.differencesMatch(2, 10, 495, student_Match, school_Match)
num_students_change, num_schools_change = nyc.totalDifferencesMatch(student_changes, school_changes)

student_unmatched_matched, school_unmatched_matched = nyc.unmatched_matched(2, 10, 495, student_Match, school_Match)
num_students_unm_mat, num_schools_unm_mat = nyc.total_unmatched_matched(student_unmatched_matched, school_unmatched_matched)

student_original_ranks, school_original_ranks = nyc.originalRank(student_Match, school_Match, student_original_preferences, school_original_preferences)    
student_changes_orank, school_changes_orank = nyc.change_original_rank(2, 10, 495, student_original_ranks, school_original_ranks)
num_students_imp, num_schools_imp = nyc.improve_original_rank(student_changes_orank, school_changes_orank, num_students_change, num_schools_change)

print('number of students unmatched to matched')
print(num_students_change)
print('number of schools unmatched to matched')
print(num_schools_change)

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
plt.ylabel("|Students with better match|")
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
plt.ylabel("|Students with better match|")
plt.xticks([r for r in range(len(x2))], ['11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])
#plt.legend(loc="upper left")
plt.savefig('D:/Documents/CDO/CDO_project/Figures/improvement_rank_match.png')


print('code succesfull')