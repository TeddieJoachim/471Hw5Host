import numpy as np
from matplotlib import pyplot as plt

times_list = []
with open("timingsTo8Threads.txt", "r") as file:
  for line in file:
    cleaned_line = line.strip()
    if cleaned_line:  # Skips empty lines if they exist
      times_list.append(float(cleaned_line))

times = np.array(times_list)

efficiency = np.zeros(len(times_list))
for t in range(len(times)):
  efficiency[t] = times[0] / (times[t] * (t+1)) 

efficiencyToPlot = np.array(efficiency)
t = np.arange(1, len(times) + 1)


#plt.plot(t, times, marker='o')
#plt.xlabel("Number of Threads (t)")
#plt.ylabel("Time (seconds)")
#plt.title("Execution Time vs. Number of Threads")
#plt.xticks(t)
#plt.grid(True)
#plt.show()


plt.plot(t, efficiencyToPlot, marker='o')
plt.xlabel("Number of Threads (t)")
plt.ylabel("Efficiency")
plt.title("Efficiency vs. Number of Threads")
plt.xticks(t)
plt.grid(True)
plt.show()