[[_TOC_]]

# **How it works**

1.Go to any data model.
2.Right - click on a field that appear under column name in bold.
3.click on "View Actions".

![image.png](/.attachments/image-919c0792-0167-4731-bca2-d9b0c7d07077.png)

The action bar are opened with the toggle -"Contain Relevant Data"

4.Click on the toggle - the configuration will calculate and present all the DM that contain the data you choose.

![image.png](/.attachments/image-a1fabe42-a80c-4883-800e-4a27ee84d7af.png)

![image.png](/.attachments/image-e19c2eed-49b6-44c4-bab6-6f90c13a4bd3.png)

# How to enable the feature

## Allows the toggle -"Contain Relevant Data"
 
1.Go to the mysql workbench 
2.Run the query : `SELECT * FROM sqlite_metadata.system_config;`
3.Find the 'ActionsCheckResults' field.

![image.png](/.attachments/image-df3121bd-1a80-4f9d-b273-25ae81de581c.png)

If this configuration doesn't exist -
create this row -

![image.png](/.attachments/image-843bacf7-e6b8-41ba-82f0-1892d7e22aaf.png)

If it exist - make sure that the 'ConfigValue' filed is true .
If its false change it to true and click on apply. 
(When its false - the toggle doesn't appear.)
 
![image.png](/.attachments/image-569f920a-3af5-40ef-821d-3500f66ac0ad.png)

## Allow the calculation of the fields on a DM

1. Go to the mysql workbench.
2. Run the query : `SELECT * FROM sqlite_metadata.dataschema1;` 
3. Find the data model that you want to allow calculate.

![image.png](/.attachments/image-44baabb0-f602-4f39-9937-1078edd09474.png)

4. Change 'Calculate' field to 1.
5. Click on apply. 

![image.png](/.attachments/image-8f45c112-df36-446b-b1fe-6d97d0ccca13.png)
