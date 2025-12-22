# Define an identifier with Keywords
In case there is a need to define a keywords list as an identifier, for example, if the client wants to mark suspicious words on text or document like Bomb or Gun, we have 2 options to do it:
## 1. Define regex which contains all the words
e.g.: `(?i)\b(bomb|gun)\b` (notice: this will be case insensitive and will capture also Gun, BOMB)
## 2. Create or use an existing lookup in the system that will hold the words list
1. Create or use an existing lookup in the system
1. Mark identifier as "Is Entity Extraction"
1. Associate lookup to the identifier by writing the lookup name as the regular expression with "lookup_" prefix (e.g. lookup_datasources)
![image.png](/.attachments/image-ad8871f2-e9a3-4e83-9116-719372b4edfb.png)
1. Save the identifier

Note: 
1. all lookup words must be without any spaces
2. Lookup name must be without any leading or trailing spaces
3. In case one of the lookups appears as regex doesn't exist no extractions will be made for this identifier

Example:
![image.png](/.attachments/image-52207464-8219-4cb6-b3bd-b1e0f2870156.png)