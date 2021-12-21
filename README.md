# gridappsd

Step 1: Install Gridapps docker (https://gridappsd.readthedocs.io/en/master/installing_gridappsd/index.html)
#
Step 2: Run tester3.py - the different parts are commented accordingly
I am getting an error on getting to the input API part.
#

The error is as follows:

021-12-21 02:23:51,729 Thread-39 ERROR [gov.pnnl.goss.gridappsd.log.LogManagerImpl] - 1640053431729|helics_goss_bridge.py|789771196|ERROR|system|ERROR
An error occured while trying to translate the update message received
Traceback (most recent call last):
  File "/gridappsd/services/helicsgossbridge/service/helics_goss_bridge.py", line 748, in _publish_to_helics_bus
    raise RuntimeError(f"Forward difference command cannot be parsed correctly one or more of attributes needed was None.\ndifference:{json.dumps(x,indent=4,sort_keys=True)}\nparsed result:{json.dumps(parsed_result,indent=4,sort_keys=True)}")
RuntimeError: Forward difference command cannot be parsed correctly one or more of attributes needed was None.
difference:{
    "attribute": "Switch.open",
    "object": "_2858B6C2-0886-4269-884C-06FA8B887319",
    "value": 1
}
parsed result:{
    "cim_attribute": "Switch.open",
    "object_name": null,
    "object_name_prefix": null,
    "object_phases": null,
    "object_property_list": null,
    "object_total_phases": null,
    "object_type": null
}
