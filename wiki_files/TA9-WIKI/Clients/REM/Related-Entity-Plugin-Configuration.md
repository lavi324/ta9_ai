**Plugin Specs** - https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7b7282DC69-B32A-4185-9B45-277731526432%7d&file=%D7%90%D7%A4%D7%99%D7%95%D7%9F%20%D7%A4%D7%9C%D7%90%D7%92%D7%99%D7%9F%20%D7%99%D7%A9%D7%95%D7%99%D7%95%D7%AA%20%D7%9E%D7%A7%D7%95%D7%A9%D7%A8%D7%95%D7%AA.docx&action=default&mobileredirect=true

# Package Content

Should be put inside the proper path in `dataconnectionmanager`. Usually it is on `\TA9\C#\TA9 Core Services\Plugins\DM`

![image.png](/.attachments/image-21d8add0-b2f3-49c2-8f03-0e5e5ea2b7f8.png)

# Configurations
![image.png](/.attachments/image-9c28d7dd-c2ee-4742-90da-a6e3c1ff6e00.png)

## All following highlighted points should be changed in the configuration file: 
{
  "Entities": {
    "UnusualEventsEntityType": "**EN67**",
    "UnusualEventsCatchTypePropertyName": "**EP67_10**",
    "UnusualEventsCargoDescriptionPropertyName": "**EP67_5**",
    "NewsEntityType": "**EN83**",
    "NewsSourceTypePropertyName": "**EP83_4**",
    "NewsSubjectPropertyName": "**EP83_9**"
  },
  "OrientDb": {
    "OrientServerHost": "**http://10.100.102.61**",
    "OrientPort": **2480**,
    "OrientUser": "**root**",
    "OrientPassword": "**orient!@#$**",
    "OrientDatabaseName": "**TA9**",
    "OrientRelationTableName": "**RL0**"
  },
  "Misc": {
    "ServerUrl": "**http://10.100.102.60/api**",
    "EntityUrlPrefix": "**http://10.100.102.60/#/entity/view/**",
    "WhereCluase": "**out**"
    /* 
    WhereCluaseIn:  "in" - In case RL0 is normal
    WhereCluaseOut: "out" - In case RL0 is inverted
    */
  }
}

# Data Model Query 
should be configured like this:
![image.png](/.attachments/image-c588db25-b7cb-4bf4-a9a4-5f43e577cd85.png)

The following parameters should be set:
1. Condition וגם in the main query
2. "טווח זמנים" parameter in the main query
3. 2 groups that contain 2 conditions each:

First group:
   * ארוע חריג סוג מטען
   * ארוע חריג סוג תפיסה 
 
Second Group:
   * ידיעה נדון
   * ידיעה סוג מקור 

![image.png](/.attachments/image-02ce728a-15e5-4528-8211-5a64b964bb17.png)