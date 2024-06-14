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
miu_service = 1
T_total = 60


class Job (threading.Thread):
   def __init__(self, ID):
      threading.Thread.__init__(self)
      self.ID = ID
      self.Start_time = -1
      self.End_time = -1
   def run(self):
      global service_full
      waiting_queue.append(self.ID)
      self.Start_time = time.time()
      print("Added job in Queue: " + str(self.ID))
      while(waiting_queue[0]!= self.ID):
          pass
      print("Job ready for service: " + str(self.ID))
      while (service_full == True):
          pass
      service_full = True
      T_process=random.exponential(1/miu_service)
      print("Service started for job: " + str(self.ID))
      time.sleep(T_process)
      print("Service finished for job: " + str(self.ID) )
      service_full = False
      self.End_time = time.time()
      waiting_queue.pop(0)
      job_time.append((self.ID ,
                       self.Start_time,
                       self.End_time,
                       float(self.End_time) -  float(self.Start_time)))



def simulation_MM1(lambda_interval):
   first_job = Job(0)
   first_job.start()
   T_Interval=random.exponential(1/lambda_interval)
   time.sleep(T_Interval)
   t_end = time.time() + 60
   i=1
   while(time.time()<t_end):
      T_Interval = random.exponential(1/lambda_interval)
      time.sleep(T_Interval)
      job = Job(i)
      jobs.append(job)
      job.start()
      i+=1
   sum = 0
   time.sleep(120)
   for j in job_time:
      sum+=j[3]
   print("Average time is: " + str(sum / len(job_time)))
   return sum / len(job_time)

output = []

lambda_int = [0.1 , 0.2 , 0.3 , 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for i in lambda_int:
    output.append(simulation_MM1(i))
    print("################### Sim "+ str(i) + " finished")


plt.plot(np.array(lambda_int), np.array(output))
plt.show()