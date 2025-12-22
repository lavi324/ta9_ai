# Suzuki PLA
The previous solution was similar to the logic we have in IOC. It meant that once an incident is inserted into PLA, there is no way to track if the process failed or not.

The new design introduces a queue to PLA: PLA inserts the data into the queue, and another process responds to insert the data into the entity's service. If the process fails, the data can be inserted again into the original queue, allowing us to track and analyze why it failed. In some cases, manual insertion into the system is also possible.

Since the insertion is now outside the PLA scope, a challenge arises regarding how the new service receives the Token and Gateway URL.
The solution is to pass the token with incident data. In the future, we will consider a more elegant solution for this.


<IMG  src="https://dev.azure.com/ta-9/3a248dc3-7a86-4c67-af7a-cf12af3d5126/_apis/wit/attachments/4db5b36f-a5a4-40b6-95d6-195855542c82?fileName=image.png"  alt="Image"/>

*Written by Alex