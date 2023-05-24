import statistics as s
import matplotlib.pyplot as plt
import numpy as np


num_honeypot = 2
service_number = [0, 1, 10, 20, 30, 40]
service_number1 = [0, 1, 5, 15, 25, 35]
service_no_MTD = [0, 1, 1, 1, 1, 1]
service_MTD = []

avg_service_1 = 0
avg_service_10 = 0
avg_service_20 = 0
avg_service_30 = 0
avg_service_40 = 0

service_first_1 = [0, 0, 0, 0, 0, 1]

service_first_10 = [5, 2, 7, 2, 6, 8]

service_first_20 = [15, 8, 8, 1, 8, 2, 4, 2, 7, 8, 18, 2, 8]

service_first_30 = [5, 6, 0, 5, 11, 8, 20, 13, 8, 15, 3, 12, 12]

service_first_40 = [23, 12, 12, 22, 3, 20, 16, 35, 11, 20, 8, 23]


avg_service_1 = s.mean([service_first_1[0], service_first_1[1], service_first_1[2], service_first_1[3], 
                        service_first_1[4], service_first_1[5]])
avg_service_10 = s.mean([service_first_10[0], service_first_10[1], service_first_10[2], service_first_10[3],
                         service_first_10[4], service_first_10[5]])
avg_service_20 = s.mean([service_first_20[0], service_first_20[1], service_first_20[2], service_first_20[3],
                         service_first_20[4], service_first_20[5], service_first_20[6], service_first_20[7],
                         service_first_20[8], service_first_20[9], service_first_20[10], service_first_20[11]])
avg_service_30 = s.mean([service_first_30[0], service_first_30[1], service_first_30[2], service_first_30[3],
                         service_first_30[4], service_first_30[5], service_first_30[6], service_first_30[7],
                         service_first_30[8], service_first_30[9], service_first_30[10], service_first_30[11]])
avg_service_40 = s.mean([service_first_40[0], service_first_40[1], service_first_40[2], service_first_40[3],
                         service_first_40[4], service_first_40[5], service_first_40[6], service_first_40[7], 
                         service_first_40[8], service_first_40[9], service_first_40[10], service_first_40[11]])

service_MTD = [0, avg_service_1, avg_service_10/10, avg_service_20/20, avg_service_30/30, avg_service_40/40]

service_MTD = np.interp(service_number1, service_number, service_MTD)

plt.plot(service_number, service_MTD, label = 'MTD and AD')
plt.plot(service_number, service_no_MTD, linestyle='dotted', label = 'AD')
plt.xlabel("Real Services (number)")
plt.ylabel("Avg. Discovered Real Services (number)")
plt.xlim(0, 40)
#plt.ylim(0, 40)
plt.title("Avg. of Discovered Real Services over Real Services (Honeypot Number = 2)")
plt.legend()
plt.show()


