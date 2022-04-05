import unbalanced_matching as um
import matplotlib.pyplot as plt

men_pref_sizes = list(range(5,151))

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

print('code succesfull')