import unbalanced_matching as um
import counselor_matching as cm
import real_change_on_rank as rc
import nyc_school_market as nyc
import matplotlib.pyplot as plt

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

student_f_pref, school_f_pref = nyc.MarriageMarketPreferenceLists(100, 101)
student_pre, school_pre = nyc.RestrictedMarket(5, student_f_pref, school_f_pref)
student_sp, school_sp = nyc.galeShapleyModified(100, 101, student_pre, school_pre)

print(student_sp)

print(school_sp)

print('code succesfull')