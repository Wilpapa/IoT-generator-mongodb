# IoT-generator-mongodb
 
__Generates bucketed IoT temperature data__

---
## Description

This proof shows how MongoDB supports strongly consistent reads and writes in a sharded environment even when reading from secondaries.

The proof uses randomly generated persons data (people records each with _firstname_, _lastname_, _age_, _addresses_ and _phones_ fields, plus other fields). The main test continuously updates the _age_ field of random people via replica-set primaries and then reads the _age_ field value back for each corresponding updated person records via the replica-set secondary, verifying that the values match each time. The following MongoDB driver settings are used: _writeConcern:majority_, _readConcern:majority_, _readPreference:secondaryPreferred_, _retryableWrites:true_, _causal consistency enabled_. During the test run, a failover is induced via the Atlas _Test Failover_ feature to check that strong consistency is still achieved, even when servers fail.

 _About the run environment_: This proof requires high read and write rate. It's strongly advised that all scripts are executed in an AWS EC2 VM running in the same region as your ATLAS Cluster.

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

pass the URI as a parameter :

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
