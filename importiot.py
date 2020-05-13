#!/usr/bin/env python3
# call with parameter: MongoDB URI.

import random
import sys
import time
import statistics  
import pprint
import datetime
from _datetime import date,timedelta
from multiprocessing import Process
from pymongo import MongoClient, WriteConcern

# Number of processes to launch
processesNumber = 16
processesList = []

# constants
deviceList = ["PTA101","PTA299","BRA001","FRZ191","FRB980","AUS009","JPY891","JPY791","ITI112","SPL556","UKA198","NLO220","DEO987","ISO008","RUA177","CAR788","USH401","USJ465"]
startDate = datetime.datetime(2020,1,1) # first day to inject data
days = 140 # number of days to inject

# Returns a new temperature using delta and min/max values
def changeTemp(temp,min,max,delta):
    variation=random.randint(0,delta)-(delta/2)
    if (temp+variation > max) or (temp+variation < min):
        temp = temp - variation
    else:
        temp = temp + variation
    return temp

# Main processes code
def run(process_id, uri):
    
    id=deviceList[process_id]
    print("process", process_id, "connecting to MongoDB... for device ",id)
    connection = MongoClient(host=uri, socketTimeoutMS=10000, connectTimeoutMS=10000, serverSelectionTimeoutMS=10000)
    iot_collection = connection.world.get_collection("iot", write_concern=WriteConcern(w=1, wtimeout=8000))

    for j in range(days):
        currentDate = startDate + timedelta(days=j)
        temp = random.randint(17,23)
        for i in range(24):
            missed = random.randint(0,3) #simulates missing measures
            
            values = []
            tempList = []
            for k in range(60-missed):
                values.append({ "measureMinute":k,"measuredValue": temp})
                tempList.append(temp)
                temp = changeTemp(temp,13,29,5)
            
            doc = {
                "id" : deviceList[process_id],
                "measureDate" : currentDate + timedelta(hours=i),
                "measureUnit" : "°C",
                "periodAvg" : statistics.mean(tempList),
                "periodMax" : max(tempList),
                "periodMin" : min(tempList),
                "missedMeasures" : missed,
                "recordedMeasures" : 60-missed,
                "values" : values
                }
            #pprint.pprint(doc)
            iot_collection.insert_one(doc)
            print('%s - process %s - id %s - date %s' % (time.strftime("%H:%M:%S"), process_id, id, currentDate))
        

# Main
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You forgot the MongoDB URI parameter!")
        print(" - example: mongodb://mongo1,mongo2,mongo3/test?replicaSet=replicaTest&retryWrites=true")
        print(" - example: mongodb+srv://user:password@cluster0-abcde.mongodb.net/test?retryWrites=true")
        exit(1)
    mongodb_uri = str(sys.argv[1])

    print("launching", str(processesNumber), "processes...")

    # Creation of processesNumber processes
    for i in range(processesNumber):
        process = Process(target=run, args=(i, mongodb_uri))
        processesList.append(process)

    # launch processes
    for process in processesList:
        process.start()

    # wait for processes to complete
    for process in processesList:
        process.join()
