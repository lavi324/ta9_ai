
# Overview
_IntSight allows adding multiple custom system languages. The default language is English, but the system supports multiple custom languages._

## Languages Table
The "sqlite_metadata.languages" table contains system languages, identified by a language code, and supports LTR and RTL directions.

![image.png](/.attachments/image-5785bfb4-0ee0-436f-893f-417900a272b7.png)
## Language Translation Table
The "sqlite_metadata.language_translation" table stores keys and values for items and their translations. The Trans_1, Trans_2, etc., columns are read from the "sqlite_metadata.languages" table corresponding to the language ID. For example, if the ID for Hebrew is 2, the "Trans_2" column will hold the translation values for Hebrew.

![image.png](/.attachments/image-45cc392a-1362-4257-8e46-63f878204b29.png)


# Process
1. Insert a new record into the "sqlite_metadata.languages" table.
2. Enter the language code (e.g., he-IL), the language name (which will be displayed when selecting the language on the login page), the text direction (RTL or LTR), and a flag.
3. Save the changes.
4. Create the "trans_2" column in the "sqlite_metadata.language_translation" table.
5. Insert translation values into the "trans_2" column in the "sqlite_metadata.language_translation" table.