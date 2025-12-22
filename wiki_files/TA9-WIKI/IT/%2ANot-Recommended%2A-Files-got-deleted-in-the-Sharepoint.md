[[_TOC_]]
# Download PnP.powershell
Open powershell as administrator, then install PnP.powershell using the next command.
`Install-Module -name PnP.PowerShell`
Say yes to all.
![image.png](/.attachments/image-2ce1d328-18b1-4f63-9d49-f1505ef8ee88.png)

#Connect your account
You will need to have admin priviliges for the folder/shared file that you want to restore.
After you download you will need to connect the pnp to the relevant site.
In this example i will use Business Team.
Use the nex command to connect to your site:
`Connect-PnPOnline -Url "https://(Site_Name)" -interactive`
![image.png](/.attachments/image-7cf487eb-781d-42b0-88f8-93fa92a714b0.png)

#Check items
Before restoring items for the recyecle bin lets check to see if we got the item/s that we want.
use the next command to print the item/s that you would like to restore.
`Get-PnPRecycleBinItem -SecondStage | ? -Property dirname -like "(Item/s_to_restore)"`
![image.png](/.attachments/image-021ba39d-ccf8-4901-bbe9-e20c1b3d6a14.png)

#Restore items
After you confiremed that your found your item/s that you want to restore are in the recycle bin you ready to restore them.
Use the next command to restore the files.
`Get-PnPRecycleBinItem -SecondStage | ? -Property dirname -like "(Item/s_to_restore)" | Restore-PnPRecycleBinItem -force`
This command will take a while if you take good amount of items.