Sometimes a reference go bad on SourceTree and you can't fetch or pull.
The error reads as follows: "unable to resolve reference, reference broken"

![image.png](/.attachments/image-b0f065cd-9758-4264-8f34-d32b1c65329b.png)

* Go to Git Bash:
![image.png](/.attachments/image-4c955118-1b61-4615-a0f8-2c8af6d1d1d4.png)

* Navigate to your local needed repository (where the bad reference branch dwells):
![image.png](/.attachments/image-3a5e9e28-de05-418e-93d4-83f978bd93e9.png)

* It should look like this: 
![image.png](/.attachments/image-ba5bf09c-2ac5-4b4f-99e3-5d445563f57c.png)

* Remove the needed branch, you can write the path till the number of the branch and then just Tab it for a nice auto-complete:
![image.png](/.attachments/image-3af755da-c191-44fe-bd79-e35fda8739c1.png)

* Git Fetch now, it should recognize the missing bad (now very good) branch:
![image.png](/.attachments/image-62d12f1e-45f7-4223-9905-30c826a6aca1.png)

* Check the SourceTree, Fetch again if needed, and it should be fine.