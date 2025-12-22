In case the TA9 Service host is stuck, and won't restart, you can force shut it from the PowerShell command.

**Step 1 -** Open PowerShell app

**Step 2 -** Run the command: `Stop-Process -ID <PID>`. The process should be stopped, PowerShell indicates on the completed command run. 
>Note: put the Servide ID number in the placeholder. For example, if the service id is 1234 - the command should look like this: `Stop-Process -ID 1234`
>Note: the service PID can be found in the task manager "services" tab, under the relevant service name

**Step 3** - Go to the Services app, and start the service.