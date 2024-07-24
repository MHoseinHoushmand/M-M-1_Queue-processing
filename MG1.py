import threading
import time
from numpy import random
import numpy as np
import matplotlib.pyplot as plt

waiting_queue = []
exitFlag = 0
job_id = 0
jobs = []
job_time = []
service_full = False
miu_service = 8
T_total = 120
started_job = 0
finished_job = 0

def Theoretical_MG1_T(miu_service,x):
    return (4/miu_service) + ( (x*12/pow(miu_service,2)) / (1- 4*x/miu_service) )


class Job (threading.Thread):
   def __init__(self, ID):
      threading.Thread.__init__(self)
      self.ID = ID
      self.Start_time = -1
      self.End_time = -1
   def run(self):
      global service_full
      global finished_job
      global started_job
      started_job += 1
      waiting_queue.append(self.ID)
      self.Start_time = time.time()
      print("Added job in Queue: " + str(self.ID))
      while(waiting_queue[0]!= self.ID):
          pass
      print("Job ready for service: " + str(self.ID))
      while (service_full == True):
          pass
      service_full = True
      T_process=random.exponential(1/(miu_service/2)) +\
                random.exponential(1/(miu_service/2))
      print("Service started for job: " + str(self.ID))
      time.sleep(T_process)
      print("Service finished for job: " + str(self.ID) )
      service_full = False
      self.End_time = time.time()
      finished_job += 1
      waiting_queue.pop(0)
      job_time.append((self.ID ,
                       self.Start_time,
                       self.End_time,
                       float(self.End_time) -  float(self.Start_time)))



def simulation_MG1(lambda_interval):
    global started_job, finished_job
    first_job = Job(0)
    first_job.start()
    T_Interval = random.exponential(1 / lambda_interval)
    time.sleep(T_Interval)
    t_end = time.time() + T_total
    i = 1
    while (time.time() < t_end):
        T_Interval = random.exponential(1 / lambda_interval)
        time.sleep(T_Interval)
        job = Job(i)
        jobs.append(job)
        job.start()
        i += 1
    while (finished_job != started_job):
        pass
    sum = 0
    started_job = 0
    finished_job = 0
    for j in job_time:
        sum += j[3]
    print("Average time is: " + str(sum / len(job_time)))
    return sum / len(job_time)


output = []

lambda_int = np.arange(0.2, miu_service + 0.2, 0.2)
for i in lambda_int:
    output.append(simulation_MG1(i))
    print("################### Sim " + str(i) + " finished")

theorical_T = Theoretical_MG1_T(miu_service, lambda_int)

plt.plot(lambda_int, np.array(theorical_T), label='Theoretical', color='blue')
plt.plot(lambda_int, np.array(output), label='Simulation', color='red')
plt.title('Average answer for miu=8')
plt.xlabel('lambda')
plt.ylabel('(Average answer(s))')
plt.legend()
plt.show()