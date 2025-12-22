[[_TOC_]]

# Tool Description
Loading incidents application create and push new incidents/events to events DM, those events can be viewed on C&C.
An example of an event which is being created:
![image.png](/.attachments/image-7f43533e-69ca-45e7-a81f-74fcb0831f95.png)

# Tool Path
The tool located at: \\10.100.102.13\Share\IT\Situations\IncidentsLoading

# Tool Activation
To activate the tool you need to run the EXE file.
The parameter can be changed from JSON file appconfig.json.

The parameters are:
1. AuthenticationService & ReportServices server IP (E.g. **http://10.100.102.220**, no Default value)
2. User name to use (E.g. **ta9admin@TA9.local**, no Default value)
3. The user password to use (no Default value)
4. Number of events to create in each Thread (Default value: 100)
5. interval between each event in seconds (Default value: 3)
6. how many threads to run simultaneously (Default value: 3) 
7. Events DM id (Default value: -3)
8. centerPoint is the center point for creating events (lat,long)
   - Go to google maps and right-click on wanted place, copy the number with 6 digits after the point
9. range for creating points. 

![image.png](/.attachments/image-03e9f6e5-b4b7-491c-8dc1-0f53198813c4.png)
So If choose: eventsToCreatePerThread "10" ,interval "5"  threads "6" 
the application will add 10 events each 5 seconds until it will reach 60 events in total (10 * 6).
The range for points is 1o so all points will be in range 10+- 5.395639 and 10+- -4.030266


# Tool source code
Located at: 
https://dev.azure.com/ta-9/Argus/_git/Utils?version=GBmaster&path=%2FLoadTests%2FIncidentsLoading
git\utils\LoadTests\IncidentsLoading

# Implementation Details
The tool is using Chance.NET - (https://github.com/gmantaos/Chance.NET) which based on ChanceJS (https://chancejs.com/) to create an event with random properties.

The events are loaded to the system using InsertBulkData.