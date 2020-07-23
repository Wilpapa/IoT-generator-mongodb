# IoT-generator-mongodb
 
__Generates bucketed IoT temperature data__

---
## Description

This script will simulate a recorded set of IoT measures (temperatures).
Each device sends a measure every minute, some measures can be missed, and measures are recording from a starting date during a number of days.

While we could save a single document for each measure, there are better ways taking advantage of the document model. In this script we are using time bucketing : each document contains up to 60 measures (1 by minute) per item per hour.

This kind of structure has several advantages
- lower document cardinality, meaning smaller indexes and less objects to process
- pre-calculated values (like avg, min, max) allowing for fast retrieval
- direct access to an hour of values (which makes sense if that's a use case)

A good practice is to use a bucketing method that matches best how data is consumed.

---
## Setup
* Ensure __Python 3__ is installed and install required Python libraries:
  ```bash
  pip3 install -r requirements.txt
  ```
* Edit importiot.py variables

startDate = datetime.datetime(2020,1,1) # first day to inject data
days = 140 # number of days to inject

you can also change __processNumber__ if you want to modify the number of concurrent processes to run (a good rule of thumb is to use 2 processes by core).
There will be as many devices recorded in the database as processes (do not exceed 16).

## Run
* Get the URI for your MongoDB Setup. 

use "localhost" for a local mongod 

use "mongodb+srv://user:password@replicasetFQDN/test" format for ATLAS server (get it using "Connect" button)

use "mongodb://user:password@hostname" for single node remote server

etc.

* pass the URI as a parameter :

```
python3 importiot.py "mongodb+srv://user:password@replicasetFQDN/test"
```

## Result

The script will create a collection called world.iot with up to 60 measures per hour per device (so 24 documents per device per day) :
```
{
	"_id" : ObjectId("5eb8fe15d1e3ecd96facb51d"),
	"id" : "BRA001",
	"measureDate" : ISODate("2020-01-03T11:00:00Z"),
	"measureUnit" : "°C",
	"periodAvg" : 22.25,
	"periodMax" : 28.5,
	"periodMin" : 14.5,
	"missedMeasures" : 0,
	"recordedMeasures" : 60,
	"values" : [
		{
			"measureMinute" : 0,
			"measuredValue" : 23
		},
		{
			"measureMinute" : 1,
			"measuredValue" : 22.5
		},
		{
			"measureMinute" : 2,
			"measuredValue" : 22
		},
(etc.)
}
```
