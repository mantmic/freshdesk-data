# scripts to generate random activity

from numpy.random import normal
from datetime import timedelta, datetime

from config import time_delta_mean
from config import time_delta_std

#function to return a random start time
def getActivityStartTime():
    return datetime.now()

#function to return a random amonut of delta time based on a mean and std
def getActivityTimeDelta(mean,std):
    delta = -1
    #keep getting random numbers until > 0
    while delta <= 0:
        delta =  normal(mean,std)
    return(timedelta(minutes = delta))

#returns the required activity after a random amount of time
def getActivity(status, baseTs):
    return({
        'status':status,
        'performed_at':baseTs + getActivityTimeDelta(time_delta_mean,time_delta_std)
    })
