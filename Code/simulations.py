import unbalanced_matching as um
import matplotlib.pyplot as plt

rank_size_men, rank_size_women = um.simulationMCMatching(1000, 1001, [5, 50, 100, 150], 1000, 5)

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
plt.show()

print('code succesfull')