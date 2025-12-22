available from v. 4.2.3

https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7B286C885E-7DD0-4003-9B3E-4126FF1BE799%7D&file=Prompt%20Drone%20Incidents%20DC.docx&action=default&mobileredirect=true

### TOASTS 
Every time a query is done (changing the time range, refreshing the data), incidents will render, and a toast will pop up with the number of drone incidents that happened in the ‘new’ query.  

1. Incident list automatic update (configurable) - The incident list is updated every 30 seconds (depending on the configuration), so if a new drone incident is received, a new toast will pop. 

1. Permissions - The toast will be available to all users with permission to the incidents DM. 

1. Availability - The toast will be available only if the user is in the situational picture. 

1. Visual appearance - The toast has a visual appearance only, without sound. 

1. Update rule - The rule is the user will receive a toast every refresh or every new time range query on every drone incident. The only factor for receiving toasts for drone incidents will be the time range. In case the user didn’t query a specific time range in the past, and is focusing on the last 30 min, he will receive toast for real-time drone incidents, regardless of the location he is focusing on. 

1. Time range dependency - If the user monitors a specific time range (which does not last 30 min), and the incident happens outside that range, they will not receive a toast: in case the user is targeting a specific time range (for example, the user queries a specific day that occurred 2 months ago), there will be no toast popping up if a new drone incident is received in real-time. Since the user chose to query a different time range. 

1. Date/time field - The date/time field to calculate the refresh is the Report time.


### NEW FIELD IN MESSAGE BROKER 

To identify drone incidents, a new field will be added to message broker. 

TA9 will develop the first business logic/ code in the message broker for drones. ST to take over the maintenance of the business logic moving forward.  