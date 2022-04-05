import unbalanced_matching as um
import matplotlib.pyplot as plt

men_pref_sizes = list(range(5,151))

'''
rank_size_men, rank_size_women = um.simulationMCMatching(1000, 1001, men_pref_sizes, 1000, 500)

print(rank_size_men)
print(rank_size_women)

lists1 = sorted(rank_size_men.items()) # sorted by key, return a list of tuples
lists2 = sorted(rank_size_women.items())
x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples
x2, y2 = zip(*lists2)
plt.plot(x1, y1, label='Rank_Students')
plt.plot(x2, y2, label='Rank_Schools')
plt.xlabel("Average rank")
plt.ylabel("Average degree d")
plt.legend(loc="upper left")
plt.savefig('D:\Documents\CDO\CDO_project\rank_diff_pref_sizes.png')
'''
student_pref_sizes = list(range(5,151))
rank_size_students, rank_size_schools, rank_size_students_2, rank_size_schools_2 = um.simulationPreferenceAdditions(1000, 1001, student_pref_sizes, 1000, 1, 3, .9, 5)

print(rank_size_students)
print(rank_size_schools)
print(rank_size_students_2)
print(rank_size_schools_2)

lists1 = sorted(rank_size_students.items()) # sorted by key, return a list of tuples
lists2 = sorted(rank_size_schools.items())
x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples
x2, y2 = zip(*lists2)
lists1_2 = sorted(rank_size_students_2.items()) # sorted by key, return a list of tuples
lists2_2 = sorted(rank_size_schools_2.items())
x1_2, y1_2 = zip(*lists1_2) # unpack a list of pairs into two tuples
x2_2, y2_2 = zip(*lists2_2)
plt.plot(x1, y1, label='Rank_Students')
plt.plot(x2, y2, label='Rank_Schools')
plt.plot(x1_2, y1_2, label='Rank_Students_2')
plt.plot(x2_2, y2_2, label='Rank_Schools_2')
plt.xlabel("Average rank")
plt.ylabel("Average degree d")
plt.legend(loc="upper left")
plt.show()


print('code succesfull')