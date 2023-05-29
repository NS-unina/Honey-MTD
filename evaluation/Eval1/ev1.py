import statistics as s
import matplotlib.pyplot as plt
import numpy as np

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 13

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=BIGGER_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

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

service_first_1 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

service_first_10 = [5, 2, 7, 2, 6, 8, 0, 0, 0, 0, 0, 0]

service_first_20 = [15, 8, 8, 1, 8, 2, 4, 2, 7, 8, 18, 2]

service_first_30 = [5, 6, 0, 5, 11, 8, 20, 13, 8, 15, 3, 12]

service_first_40 = [23, 12, 12, 22, 3, 20, 16, 35, 11, 20, 8, 23]

services = [service_first_1, service_first_10, service_first_20, service_first_30, service_first_40]


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

service_MTD = [0, avg_service_1, avg_service_10, avg_service_20, avg_service_30, avg_service_40]

# diff1 = 0
# diff2 = 1 - avg_service_1
# diff_3 = 10 - avg_service_10
# diff_4 = 20 - avg_service_20
# diff_5 = 30 - avg_service_30
# diff_6 = 40 - avg_service_40

# diff = [diff1, diff2, diff_3, diff_4, diff_5, diff_6]
# print(diff)

# calcolo varianza
# varianze = []
# for j in range(0, len(services)):
#     var = 0
#     sum = 0
#     for i in range(0, len(service_first_1)):
#         dif = services[j][i] - service_MTD[j + 1]
#         dif = dif*dif
#         sum = sum + dif
#     var = sum/len(service_first_1)
#     varianze.append(var)

# confidence interval 95%
dev_std = []
int_conf = []
upper = [0]
down = [0]
z = 1.96
for j in range(0, len(services)):
    dev = np.std(services[j])
    dev_std.append(np.std(dev))
    x = (abs(dev/np.sqrt(len(service_first_1))))*z
    int_conf.append(x)
    upper.append(service_MTD[j + 1] + x)
    down.append(service_MTD[j + 1] - x)

service_MTD = np.interp(service_number1, service_number, service_MTD)
upper = np.interp(service_number1, service_number, upper)
down = np.interp(service_number1, service_number, down)

plt.figure(figsize=(10, 6))
plt.plot(service_number, upper, color='b', alpha=0.10, label = 'mean_a upper bound, I.C. 95%')
plt.plot(service_number, down, color='b', alpha=0.10, label = 'mean_a lower bound, I.C. 95%')
plt.plot(service_number, service_MTD, color='b', label = 'mean_a = mean of discovered services with Moving Target and Active Deception')
plt.fill_between(service_number, upper, down, color="b", alpha=0.15)
plt.plot(service_number, service_no_MTD, color='r', linestyle='dotted', label = 'mean_b = mean of discovered services with Active Deception')
plt.xlabel("Real Services (number)")
plt.ylabel("Avg. Discovered Real Services (number)")
plt.xlim(0, 40)
plt.ylim(0, 40)
plt.title("Avg. of Discovered Real Services over Real Services (Honeypot Number = 2)")
plt.legend(fontsize="8")
plt.show()
#plt.savefig('./ev1.png')

