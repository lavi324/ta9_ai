**portal-favorite-items.json**

![image.png](/.attachments/image-aa1a9316-8db2-4dff-982c-801401095d56.png)

The file is built out of 3 parts: module, ID and isFixed.

**module**

This means the type of application you want to be shown on the recent app widget by this order - 
Unknown = 0
Form = 1
App = 2
Dashboard = 3
DataModel = 4
Feed = 5
Entity = 6
Group = 7
Case = 8
Favourites = 9
Admin = 10
Category = 11
newDashboard = 12

**ID**

This means the ID of the specific ID from your type of module you chose. For example if you would like to choose the genral case to be shown on the recent apps widget you would type module=8 and ID=-1.

**isFixed**

This means that if you would mark isFixed as true, the tile would appear before the recent apps the were used.
Because this widget is built out of 8 tiles, if you would choose 8 fixed items, no recent apps will appear, but only the items you chose.
