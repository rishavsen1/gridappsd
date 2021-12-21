from time import sleep
import time
run_config_123 = {
    "power_system_config": {
        "GeographicalRegion_name": "_73C512BD-7249-4F50-50DA-D93849B89C43",
        "SubGeographicalRegion_name": "_1CD7D2EE-3C91-3248-5662-A43EFEFAC224",
        "Line_name": "_C1C3E687-6FFD-C753-582B-632A27E28507"
    },
    "application_config": {
        "applications": []
    },
    "simulation_config": {
        "start_time": "1570041113",
        "duration": "120",
        "simulator": "GridLAB-D",
        "timestep_frequency": "1000",
        "timestep_increment": "1000",
        "run_realtime": True,
        "simulation_name": "ieee123",
        "power_flow_solver_method": "NR",
        "model_creation_config": {
            "load_scaling_factor": "1",
            "schedule_name": "ieeezipload",
            "z_fraction": "0",
            "i_fraction": "1",
            "p_fraction": "0",
            "randomize_zipload_fractions": False,
            "use_houses": False
        }
    },
    "model_creaion_config":{
	    "load_scaling_factor": "1",
	    "schedule_name": "ieeezipload",
	    "z_fraction": "0",
	    "i_fraction": "1",
	    "p_fraction": "0",
	    "randomize_zipload_fractions": False,
	    "use_houses": False
	},
    	
    "test_config": {
        "events": [{
            "message": {
                "forward_differences": [
                    {
                        "object": "_6C1FDA90-1F4E-4716-BC90-1CCB59A6D5A9",
                        "attribute": "Switch.open",
                        "value": 1
                    }
                ],
                "reverse_differences": [
                    {
                        "object": "_6C1FDA90-1F4E-4716-BC90-1CCB59A6D5A9",
                        "attribute": "Switch.open",
                        "value": 0
                    }
                ]
            },
            "event_type": "ScheduledCommandEvent",
            "occuredDateTime": 1570041140,
            "stopDateTime": 1570041200
        }]
    },
     "service_configs": [{
        "id": "gridappsd-sensor-simulator",
        "user_options": {
            "sensors-config": {
                "_99db0dc7-ccda-4ed5-a772-a7db362e9818": {
                    "nominal-value": 100,
                    "perunit-confidence-band": 0.02,
                    "aggregation-interval": 5,
                    "perunit-drop-rate": 0.01
                },
                "_ee65ee31-a900-4f98-bf57-e752be924c4d": {},
                "_f2673c22-654b-452a-8297-45dae11b1e14": {}
            },
            "random-seed": 0,
            "default-aggregation-interval": 30,
            "passthrough-if-not-specified": False,
            "default-perunit-confidence-band": 0.01,
            "default-perunit-drop-rate": 0.05
        }
    }]
}

import json
from gridappsd.simulation import Simulation # Import Simulation Library
from gridappsd import GridAPPSD
import time
from gridappsd.topics import simulation_input_topic
from gridappsd import topics as t

username = "system"
password = "manager"

# Note: there are other parameters for connecting to
# systems other than localhost
gapps = GridAPPSD(username=username, password=password)

assert gapps.connected



run123_config = json.load(open("Run123NodeFileSimAPI.json")) # Pull simulation start message from saved file

simulation_obj = Simulation(gapps, run123_config) # Create Simulation object
simulation_obj.start_simulation() # Start Simulation

simulation_id = simulation_obj.simulation_id # Obtain Simulation ID
print("Successfully started simulation with simulation_id: ", simulation_id)

viz_simulation_id = simulation_id

topic = simulation_input_topic(viz_simulation_id)


# for checking pause, resume
'''
while(True):

	ch = int(input())
	if ch == 1:
		message = {"command": "pause"}
		gapps.send(topic, message)
	elif ch == 2:
		message = {"command": "resume"}
		gapps.send(topic, message)
		
	else:
		exit()
'''

#delay
for i in range(30):
	sleep(1)
	print("sleeping ",i)


## giving inputs

input_topic = simulation_input_topic(simulation_id)
model_mrid = "_49AD8E07-3BF9-A4E2-CB8F-C3722F837B62"
message = {
    "modelId": model_mrid,
    "requestType": "QUERY_OBJECT_DICT",
    "resultFormat": "JSON",
    "objectType": "LoadBreakSwitch"
}

response_obj = gapps.get_response(t.REQUEST_POWERGRID_DATA, message)
switch_dict = response_obj["data"]
print(switch_dict)
sw_mrid=''

for index in switch_dict:
    if index["IdentifiedObject.name"] == 'sect1':
        sw_mrid = index["IdentifiedObject.mRID"]
print(sw_mrid)


#using Difference Builder
'''
from gridappsd import DifferenceBuilder

my_diff_build = DifferenceBuilder(simulation_id)

#my_diff_build.add_difference(sw_mrid, "Switch.open", 1, 0) # Open switch given by sw_mrid
my_diff_build.add_difference(sw_mrid, "PowerElectronicsConnection.p", 6000, 4000)

message = my_diff_build.get_message()
gapps.send(input_topic, message)
response_obj = gapps.get_response(t.REQUEST_POWERGRID_DATA, message)
switch_dict = response_obj["data"]
print(switch_dict)

'''

#using messages

message = {
  "command": "update",
  "input": {
      "simulation_id": str(simulation_id),
      "message": {
          "timestamp": int(time.time()),
          "difference_mrid": "_abcd1234",
          "reverse_differences": [{

                  "object": "_2858B6C2-0886-4269-884C-06FA8B887319",
                  "attribute": "Switch.open",
                  "value": 0
              }
          ],
          "forward_differences": [{

                  "object": "_2858B6C2-0886-4269-884C-06FA8B887319",
                  "attribute": "Switch.open",
                  "value": 1
              }
              ]
              }
      }
}

gapps.send(input_topic, message)

'''		

model_mrid = "_49AD8E07-3BF9-A4E2-CB8F-C3722F837B62"

# Create query message to obtain measurement mRIDs for all switches
message = {
    "modelId": model_mrid,
    "requestType": "QUERY_OBJECT_MEASUREMENTS",
    "resultFormat": "JSON",
    "objectType": "LoadBreakSwitch"
}




#delay
for i in range(30):
	sleep(1)
	print("sleeping ",i)
	
	
##for getting measured values

while True:
	# Pass query message to PowerGrid API Models
	response_obj = gapps.get_response(t.REQUEST_POWERGRID_DATA, message)
	measurements_obj = response_obj["data"]
	switch_dict = response_obj["data"]
	print(switch_dict)
	''
	
	# Filter to get mRID for switch SW2:
	for index in switch_dict:
		if index["IdentifiedObject.name"] == 'sw2':
			sw_mrid = index["IdentifiedObject.mRID"]

	print(switch_dict[0]) # Print dictionary for first switch

	print('mRID of sw2 is ',sw_mrid)
	''
	sleep(2);
	

# Define global python dictionary of position measurements
global Pos_obj
Pos_obj = [k for k in measurements_obj if k['type'] == 'Pos']

''
# Define global python dictionary of phase-neutral-voltage measurements (PNV)
global PNV_obj
PNV_obj = [k for k in measurements_obj if k['type'] == 'PNV']

# Define global python dictionary of volt-ampere apparent power measurements (VA)
VA_obj = [k for k in measurements_obj if k['type'] == 'VA']

# Current measurements (A)
A_obj = [k for k in measurements_obj if k['type'] == 'A']		


def demo_onmeas_func(sim, timestamp, measurements):

    open_switches = []
    for index in Pos_obj:
        if index["measid"] in measurements:
            mrid = index["measid"]
            power = measurements[mrid]
            if power["value"] == 0:
                open_switches.append(index["eqname"])

    print("............")
    print("Number of open switches at time", timestamp, ' is ', len(set(open_switches)))
    
simulation_obj.add_onmesurement_callback(demo_onmeas_func)
'''		

