import Eval1.ev1 as ev1
import Eval2.ev2 as ev2
import matplotlib.pyplot as plt

service_number_1 = ev1.service_number
service_MTD_1 = ev1.service_MTD
upper_1 = ev1.upper
down_1 = ev1.down
service_no_MTD_1 = ev1.service_no_MTD


hp_number_2 = ev2.hp_number
service_MTD_2 = ev2.service_MTD
upper_2 = ev2.upper
down_2 = ev2.down
hp_no_MTD_2 = ev2.hp_no_MTD


fig, (p1, p2) = plt.subplots(1, 2)
p1.plot(service_number_1, upper_1, color='b', alpha=0.10, label = 'mean_a upper bound, I.C. 95%')
p1.plot(service_number_1, down_1, color='b', alpha=0.10, label = 'mean_a lower bound, I.C. 95%')
p1.plot(service_number_1, service_MTD_1, color='b', label = 'mean_a = mean of discovered services with Moving Target and Active Deception')
p1.fill_between(service_number_1, upper_1, down_1, color="b", alpha=0.15)
p1.plot(service_number_1, service_no_MTD_1, color='r', linestyle='dotted', label = 'mean_b = mean of discovered services with Active Deception')
p1.set_xlabel("Real Services (number)")
p1.set_ylabel("Avg. Discovered Real Services (number)")
p1.set_xlim(0, 40)
p1.set_ylim(0, 40)
p1.set_title("Avg. of Discovered Real Services over Real Services (Honeypot Number = 2)", x=0.5, y=1.05, fontweight='bold', fontsize = 13)
p1.legend(fontsize="10")


p2.plot(hp_number_2, upper_2, color='b', alpha=0.10, label = 'mean_a upper bound, I.C. 95%')
p2.plot(hp_number_2, down_2, color='b', alpha=0.10, label = 'mean_a lower bound, I.C. 95%')
p2.plot(hp_number_2, service_MTD_2, color='b', label = 'mean_a = mean of discovered services with Moving Target and Active Deception')
p2.fill_between(hp_number_2, upper_2, down_2, color="b", alpha=0.15)
p2.plot(hp_number_2, hp_no_MTD_2, color='r', linestyle='dotted', label = 'mean_b = mean of discovered services with Active Deception')
p2.set_xlabel("Honeypots (number)")
p2.set_ylabel("Avg. Discovered Real Services (number)")
p2.set_xlim(0, 12)
p2.set_ylim(-2, 12)
p2.set_title("Avg. of Discovered Real Services over Honeypots (Real Services = 10)", x=0.5, y=1.05, fontweight='bold', fontsize = 13)
p2.legend(fontsize="10")

plt.show()