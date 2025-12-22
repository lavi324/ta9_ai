[[_TOC_]]

# Intro
Federated search schema fields are **defined** on a System Data Model with `ID=(-40)`
These fields need to be consistent with the fields defined on '_freetextindex_' collection on Solr

Usually, these fields should not be changed, except for using a field as _quick-filter/facet._

# Configure a field to be quick-filter/facet
Each field of the federated system DM can be configured to be a _quick-filter, facet_ or both. Additionally, each can be defined to be such separately for a _Search Type_. 
### Example
For example, I can configure that '_File Type_' will be shown as facet only on _'Documents' & 'Multimedia'_. 
Another example is that I want an _Entity Type_ filter to be presented only on _'Entities'_.


## Calculation
The decision where to display a field as _Filter/Facet_ is taken depends on a value defined on that field combined with the _'Search Type'_.
The combination is done using **bitwise flags**

### Search Types
![image.png](/.attachments/image-16fe8e1e-54a9-44f0-8bf9-53e788a7f862.png)

| **Search Type** | **Value** |
|--|--|
| All  | 1 |
| Entities  | 2 |
| Documents  | 4 |
| DataModel  | 8 |
| Multimedia | 16 |

Now, in order to calculate the required value, we should do a **bitwise OR** between the required _Search Types_.
For example, if we want a field to be presented (_filter/facet_) only on _Entities_ and _Data Model_, we'll do the following calculation:
`2 | 8 = 10`

So, the general calculation is:

`SearchType1 | SearchType2 | SearchType3 | ... = RESULT_VALUE`

This `RESULT_VALUE` should be set on the field configuration as follows:

1. _Facet_ configuration: **`FieldScale`**
1. _Filter_ configuration: **`FieldSize`**

### Reversed Calculation
In order to test whether a value contains a _Search Type_, the **opposite** operation should be done. 
For example, if a field is configured with `value=63` and I want to check if it includes _Entities_, I should calculate:

`63 & 2 = 2`

Only if the result is equal to the parameter `(2)` then it's actually contained.

## Bitwise Calculator
There are many options as bitwise calculations are pretty common:
1. Online tool: http://bitwisecmd.com/
You can type there `VALUE1 | VALUE2 | VALUE3` ... and use the result (hit Enter)
You can type there `RESULT_TYPE & VALUE1` to test whether a `VALUE1` is contained in `RESULT_TYPE` (hit Enter)
1. Using Windows Calculator
Switch to 'Programmer' mode and use Bitwise operators

# Additional Relevant Configurations
1. **Lookup** - if this field is connected to a Lookup - put it on `DataEnrichmentName`
1. **Display Name** - will be shown as filter/facet title

## Adding a new Facet
Add a new line to the SQL table "InternalFreeText" (ID=-40) with the appropriate field from the Solr freetextindex schema fields which you can find in here - http://[environment_ip]/solr/#/freetextindex/schema/ 

For example:
In order to add a new facet to the FS under the document category, you should follow the following steps:
1. In the Solr look for the correspondent field (email)
![image.png](/.attachments/image-1053f5b1-5543-4465-8bf2-bde36357bc90.png)
2. In MySql add the new line according to the instructions above (calculated values in FieldScale & FieldSize)
![image.png](/.attachments/image-762fdc6e-2665-4562-947a-09bbc8e2644e.png)
3. Apply, restart the Java services (Wildfly in Linux & Windows), restart the TA9 Service, clear server & client cache and enter the system. 
4. Test yourself, you should see -
![image.png](/.attachments/image-ec00731b-99a0-4a3d-a68e-7fa25ce73cd2.png)