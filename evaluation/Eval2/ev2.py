import statistics as s
import matplotlib.pyplot as plt
import numpy as np

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 15

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=BIGGER_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=BIGGER_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

hp_number = [0, 2, 4, 8, 10, 12]
hp_number1 = [0, 1, 6, 9, 11, 15]
hp_no_MTD = [10, 10, 10, 10, 10, 10]
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

honeypots = [hp_first_2, hp_first_4, hp_first_8, hp_first_10, hp_first_12]

avg_service_1 = s.mean([hp_first_2[0], hp_first_2[1], hp_first_2[2], hp_first_2[3],
                        hp_first_2[4], hp_first_2[5]])
avg_service_10 = s.mean([hp_first_4[0], hp_first_4[1], hp_first_4[2], hp_first_4[3],
                         hp_first_4[4], hp_first_4[5]])
avg_service_20 = s.mean([hp_first_8[0], hp_first_8[1], hp_first_8[2], hp_first_8[3],
                         hp_first_8[4], hp_first_8[5]])
avg_service_30 = s.mean([hp_first_10[0], hp_first_10[1], hp_first_10[2], hp_first_10[3],
                         hp_first_10[4], hp_first_10[5]])
avg_service_40 = s.mean([hp_first_12[0], hp_first_12[1], hp_first_12[2], hp_first_12[3],
                         hp_first_12[4], hp_first_12[5]])

hp_MTD = [10, avg_service_1, avg_service_10, avg_service_20, avg_service_30, avg_service_40]

# calcolo varianza
varianze = []
for j in range(0, len(honeypots)):
    var = 0
    sum = 0
    for i in range(0, len(hp_first_2)):
        dif = honeypots[j][i] - hp_MTD[j + 1]
        dif = dif*dif
        sum = sum + dif
    var = sum/len(hp_first_2)
    varianze.append(var)

testo = ["var. 2 Honeypot", "var. 4 Honeypot", "var. 8 Honeypot", "var. 10 Honeypot", "var. 12 Honeypot"]

for i in range(len(testo)):
    print(testo[i] + " = " + str(varianze[i]))

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