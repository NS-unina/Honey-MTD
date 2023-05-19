import statistics as s
import matplotlib.pyplot as plt
import numpy as np


num_honeypot = 2
service_number = [0, 1, 10, 20, 30, 40]
service_number1 = [0, 1, 5, 15, 25, 35]
service_no_MTD = [0, 1, 10, 20, 30, 40]
service_MTD = []

avg_service_1 = 0
avg_service_10 = 0
avg_service_20 = 0
avg_service_30 = 0
avg_service_40 = 0

service_first_1 = [0, 0, 0]

service_first_10 = [7, 8, 8]

service_first_20 = [18, 20, 17]

service_first_30 = [14, 21, 10]

service_first_40 = [27, 14, 28]


avg_service_1 = s.mean([service_first_1[0], service_first_1[1], service_first_1[2]])
avg_service_10 = s.mean([service_first_10[0], service_first_10[1], service_first_10[2]])
avg_service_20 = s.mean([service_first_20[0], service_first_20[1], service_first_20[2]])
avg_service_30 = s.mean([service_first_30[0], service_first_30[1], service_first_30[2]])
avg_service_40 = s.mean([service_first_40[0], service_first_40[1], service_first_40[2]])

service_MTD = [0, avg_service_1, avg_service_10, avg_service_20, avg_service_30, avg_service_40]


service_MTD = np.interp(service_number1, service_number, service_MTD)

plt.plot(service_number, service_MTD, label = 'MTD and AD')
plt.plot(service_number, service_no_MTD, linestyle='dotted', label = 'AD')
plt.xlabel("Real Services (number)")
plt.ylabel("Avg. Discovered Real Services (number)")
plt.xlim(0, 40)
plt.ylim(0, 40)
plt.title("Avg. of Discovered Real Services over Real Services (Honeypot Number = 2)")
plt.legend()
plt.show()



