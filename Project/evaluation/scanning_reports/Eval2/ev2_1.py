import statistics as s
import matplotlib.pyplot as plt
import numpy as np

hp_number = [0, 2, 4, 8, 10, 12]
hp_number1 = [0, 1, 6, 9, 11, 15]
hp_no_MTD = [1, 1, 1, 1, 1, 1]
hp_MTD = []

avg_hp_2 = 0
avg_hp_4 = 0
avg_hp_8 = 0
avg_hp_10 = 0
avg_hp_12 = 0

hp_first_2 = [8, 5, 0, 3, 2, 0]

hp_first_4 = [2, 0, 4, 3, 4, 3]

hp_first_8 = [0, 5, 0, 3, 1, 0]

hp_first_10 = [1, 0, 0, 2, 2, 0]

hp_first_12 = [4, 0, 0, 1, 0, 0]


avg_service_2 = s.mean([hp_first_2[0], hp_first_2[1], hp_first_2[2], hp_first_2[3],
                        hp_first_2[4], hp_first_2[5]])
avg_service_4 = s.mean([hp_first_4[0], hp_first_4[1], hp_first_4[2], hp_first_4[3],
                         hp_first_4[4], hp_first_4[5]])
avg_service_8 = s.mean([hp_first_8[0], hp_first_8[1], hp_first_8[2], hp_first_8[3],
                         hp_first_8[4], hp_first_8[5]])
avg_service_10 = s.mean([hp_first_10[0], hp_first_10[1], hp_first_10[2], hp_first_10[3],
                         hp_first_10[4], hp_first_10[5]])
avg_service_12 = s.mean([hp_first_12[0], hp_first_12[1], hp_first_12[2], hp_first_12[3],
                         hp_first_12[4], hp_first_12[5]])

hp_MTD = [1, avg_service_2/10, avg_service_4/10, avg_service_8/10, avg_service_10/10, avg_service_12/10]

service_MTD = np.interp(hp_number1, hp_number, hp_MTD)

plt.plot(hp_number, service_MTD, label = 'MTD and AD')
plt.plot(hp_number, hp_no_MTD, linestyle='dotted', label = 'AD')
plt.xlabel("Honeypots (number)")
plt.ylabel("Avg. Discovered Real Services (number)")
plt.xlim(0, 12)
plt.ylim(0, 2)
plt.title("Avg. of Discovered Real Services over Honeypots (Real Services = 10)")
plt.legend()
plt.show()
