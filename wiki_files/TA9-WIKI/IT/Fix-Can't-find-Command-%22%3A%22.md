if you encountered the next screen you can procced by clicking several times SpaceBar
![image.png](/.attachments/image-c60ba8f8-0c05-4f6b-b025-c54691300498.png)

It is recommended to take a snapshot of the VM before doing any changes.
Next login into the VM with root user or user with sudooer permission.
edit the file /etc/grub2.cfg.
Find line that should look like this:
![image.png](/.attachments/image-1d8e0df2-5839-41a3-9cb6-1adc4ccf27be.png)

The lines might not be identical but look for the highlighted words.
Edit the file and remove only the highlighted words for example in the case above remove:
`: # (removed by Converter)`
Next save the edited file and restart the VM and check if the error occurs again.