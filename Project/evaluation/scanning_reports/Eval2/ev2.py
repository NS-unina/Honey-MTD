import statistics as s
import matplotlib.pyplot as plt
import numpy as np

hp_number = [0, 2, 4, 8, 10, 12]
hp_number1 = [0, 1, 6, 9, 11, 15]
hp_no_MTD = [10, 10, 10, 10, 10, 10]
hp_MTD = []

avg_hp_2 = 0
avg_hp_4 = 0
avg_hp_8 = 0
avg_hp_10 = 0
avg_hp_12 = 0

hp_first_2 = [3, 3, 4]

hp_first_4 = [2, 2, 2]

hp_first_8 = [1, 3, 3]

hp_first_10 = [2, 2, 0]

hp_first_12 = [3, 1, 2]


avg_service_1 = s.mean([hp_first_2[0], hp_first_2[1], hp_first_2[2]])
avg_service_10 = s.mean([hp_first_4[0], hp_first_4[1], hp_first_4[2]])
avg_service_20 = s.mean([hp_first_8[0], hp_first_8[1], hp_first_8[2]])
avg_service_30 = s.mean([hp_first_10[0], hp_first_10[1], hp_first_10[2]])
avg_service_40 = s.mean([hp_first_12[0], hp_first_12[1], hp_first_12[2]])

hp_MTD = [10, avg_service_1, avg_service_10, avg_service_20, avg_service_30, avg_service_40]


service_MTD = np.interp(hp_number1, hp_number, hp_MTD)

plt.plot(hp_number, service_MTD, label = 'MTD and AD')
plt.plot(hp_number, hp_no_MTD, linestyle='dotted', label = 'AD')
plt.xlabel("Honeypots (number)")
plt.ylabel("Avg. Discovered Real Services (number)")
plt.xlim(0, 12)
plt.ylim(0, 15)
plt.title("Avg. of Discovered Real Services over Honeypots (Real Services = 10)")
plt.legend()
plt.show()
