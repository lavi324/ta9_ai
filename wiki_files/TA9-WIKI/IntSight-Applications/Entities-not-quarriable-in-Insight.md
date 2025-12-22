Use case from
https://dev.azure.com/ta-9/iPolice%20Support/_boards/board/t/iPolice%20Support%20Team/Stories/?workitem=46757

The user can't query entities. 502 "Bad gateway" error appears in the event viewer.

Root cause:
- WildFly service was down and couldn't be started manually
- C driver was at full space capacity.

Solution:
- Deleting old WildFly logs from the server freed up disk space, allowing the service to be manually started.