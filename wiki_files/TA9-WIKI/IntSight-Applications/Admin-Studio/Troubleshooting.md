1. Admin doesn't write any logs to event viewer
- Verify the Windows user running the admin studio has write access to the event viewer.

2. Admin can't connect and present the following message: 'Only Administrators may login to the admin studio'
- Open event viewer for more information, in case there are no logs refer to section #1
- Verify the user is defined as admin
- Log with the same user to the web client and make sure the user has access to admin tools on the top-right menu.
- Make sure all tcp.net endpoints are accessible from the machine (not localhost) and that the following ports are open: 5000,5200,5400,5800.

3. User cannot see a data model in the 'Data Loader' (from the web client).
- Add the 'Is managed' definition to the data model (from the admin studio).
