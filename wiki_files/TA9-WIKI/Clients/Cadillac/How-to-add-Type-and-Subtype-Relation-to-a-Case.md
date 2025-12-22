Open the case window:
![image.png](/.attachments/image-f16167ce-69a0-4302-99fd-5f5a2f065df2.png)

The Type and Subtype fields have no relation between them, and the default name is "General".

## In order to add more Types and SubTypes:

1. Open the table "investigationtype" in MySQL:
![image.png](/.attachments/image-0c05c331-e823-4755-a376-845ee8e034f9.png)

- And add new TypeName (like Type2 and Type 3)
- Set a unique TypeID 
- Submit 1 in the "isvalid" column.

2. Then go to "investigationsubtype" table in MySQL:
![image.png](/.attachments/image-7fda517f-f14b-4362-8e6e-c0b1c4fac256.png)

- Put a unique SubTypeID in every row
- **"TypeID" is the number of type you wish to relate your subtype to** SubTypeName is the name you choose for your subtype
- Insert 1 in "isvalid" column.

Now you can see that there are relations between the types and subtypes:
![image.png](/.attachments/image-ca817ffe-41ab-4bcf-abeb-aeef34e124f1.png)

