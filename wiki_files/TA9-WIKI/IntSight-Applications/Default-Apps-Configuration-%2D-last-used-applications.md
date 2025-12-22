IntSight portal home screen contains a default apps widget, that is composed of 8 tiles of different apps by configuration:

![image.png](/.attachments/image-23197861-42bd-4540-90db-710dbbc94b6e.png)

The portal displays Up to 8 Latest tiles according to the latest activity, such as the following:
1. A Click on any of the following tiles: A Data Model / an App / a Dashboard / an Entity as DM (not Federated search).
2. An Entry via URL or redirect to any of the modules mentioned above.

The Items (activity) will be stored on the browsers' cache for **15 minutes**.

**In case there are fewer than 8 latest items, the remaining items will be drawn from the default configuration:**

The configuration of the default favorites is in the file "portal-favorite-items.json", it is placed in the relevant server under: 
[TA9\Web\Web Client\TA9-NG\assets\config\] 

_For example:_

![image.png](/.attachments/image-63f1f607-0fc6-4141-853d-101e56a9a12d.png)

 > The **"module"** options are:
```
App = 2
Dashboard = 3
DataModel = 4
Entity = 6
```


> The **"ID"** should be the object ID.
For entity make sure you duplicate the ID by 1000 (for example EN2 = 2000).