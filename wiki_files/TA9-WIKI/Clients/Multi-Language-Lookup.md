This Feature released on V3.9.4 allows the user to see values in lookups based on the login language selected.

**For example:** If the user's login language is “Hebrew”, the user will see the lookup values in the Hebrew translation.

![image.png](/.attachments/image-6ce1e2a6-b94d-4457-84cc-b4c985c345bc.png)

# How to create Multi-Language Lookup (Data Base Configuration)

## Step 1 – Creating the table in the MySQL database (or external)

The table must include the following columns:

- Key

- Value

- Translations - Column for each language you want, with the following title format for each column: “_fr” / “_gr” / etc.

**For example,** If “value” column in the lookup is 'Name' the lookup structure should look as the following:

ID Status Status _fr Status _us Status _he

![image.png](/.attachments/image-e2853cc1-2f78-4f4a-a420-c749f14e6c2c.png)



**Note:**

- The user will see only the translation columns in the lookups, and not the value.

- If the table already exists, you can go to this table and edit it with the additional columns as the translations you have in the system.

## Step 2 – Creating the Lookup in Admin Studio (Admin)

Create a lookup via Admin Studio with the table you created. If the lookup already exists, continue to step 3.

## Step 3 – Mapping

_Before you start!_

If the lookup table exists - steps 3+4 needs to be done on the data base.

If its a new lookup configuration can be done on Admin Studio.

In this step we will map the language code in the system to the column title in the lookup using a dedicated column in lookupmanager table in IntSight Database named 'MultiLanguageMapping' (or In the field 'Language Mapping' in admin studio in lookup manager application when creating a new lookup)

In the dedicated field - Add the mapping between the lookup columns and the languages like so:

{"LanguageCode":"LookupLanguage"}

**Note:** LookupLanguage = the column title in the lookup after the underscore:

![image.png](/.attachments/image-4c72b7da-fc60-48de-b083-a5a90418273d.png)

**Examples:**

{"en-US":"us","Hebrew":"he",”French”:”fr”}

How it looks in the data base:

_Languages table_ 
![image.png](/.attachments/image-d622176d-4141-42aa-b4ad-37551ebb91a2.png)
_lookup manager table_
![image.png](/.attachments/image-9ebe357e-caf1-41f9-9728-194b93bebf5f.png)


## Step 4 – Final configuration for “is multi language lookup”

- In a new lookup - check the 'IS Multilanguage' property in the admin studio application

- If editing an existing lookup insert '1' in the "IsMultilookup" field:
![image.png](/.attachments/image-368d5730-82c3-45ea-be17-df8699fd9416.png)

**Testing**

- Login to IntSight in the required language and open an entity where the multi language lookup has been defined.

- Open the data model / entity property and confirm the lookup values appears in the logged in **language.**