import time
from numpy import random
import numpy as np
import matplotlib.pyplot as plt
job_num = 100000
miu_service = 8
service_t = job_num * [0]
arival_t = job_num * [0]
enter_service_t = job_num * [0]
leave_service_t = job_num * [0]
time_spend = job_num * [0]

def Theoretical_MM1_T(miu_service,x):
    return 1/(miu_service-x)



def MM1_ofline(lambda_rate,miu_service):
    global service_t,arival_t,enter_service_t,leave_service_t,time_spend
    for i in range(job_num):
        service_t[i] = random.exponential(1 / miu_service)
    for i in range(1,job_num):
        arival_t[i] = arival_t[i - 1] + random.exponential(1 / lambda_rate)
    leave_service_t[0] = service_t[0]
    for i in range(1,job_num):
        if leave_service_t[i-1]< arival_t[i]:
            enter_service_t[i] = arival_t[i]
        else:
            enter_service_t[i] = leave_service_t[i-1]
        leave_service_t[i] = enter_service_t[i] + service_t[i]
    for i in range(job_num):
        time_spend[i] = leave_service_t[i] - arival_t[i]
    return sum(time_spend)/len(time_spend)

output = []
lambda_int = np.arange(0.05, miu_service, 0.5)
for i in lambda_int:
    output.append(MM1_ofline(i, miu_service))


theorical_T = Theoretical_MM1_T(miu_service,lambda_int)

plt.plot(lambda_int,np.array(theorical_T),label = 'Theoretical',color='blue' )
plt.plot(lambda_int, np.array(output),label = 'Ofline_MM1_Simulation' ,color='red')
plt.title('Average answer for miu=8')
plt.xlabel('lambda')
plt.ylabel('(Average answer(s))')
plt.legend()
plt.show()