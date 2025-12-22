**Behavior:** 
2FA is activated unintentionally \ automatically for users. 
Users' complaints described a scenario where disabling the 2FA for all users only lasted for some time and that after a certain amount of time, the 2FA was enabled again without any user action prompting it.

**Symptoms:**
Users disable their 2FA authentication via the 'Users' table in MySql, changing the value under the 'Enable2FactorAuth' column to 0, disabling the 2FA for each specific user. Without any user prompting a change via DB or admin, the 'Enable2FactorAuth' is changed to 1 for several users, enabling their 2FA authentication. 

**Root cause & solution:**
in the MySql table 'system_config' under column 'ConfigKey' there's an attribute named 'TwoFactorAuthenticationMode'. It can have values from 0 to 3. 
none - 0
default not selected - 1
default selected - 2
Mandatory - 3
The value in the system_config was set to 3, causing the configuration under the 'users' table to be changed automatically. 