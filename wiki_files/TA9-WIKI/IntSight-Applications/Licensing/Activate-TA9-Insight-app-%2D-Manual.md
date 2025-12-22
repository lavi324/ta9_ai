[[_TOC_]]

#How to activate the product?
Get a license key from our sell team.

1. Open MySQL workbench.

2. Connect to the relevant DB.

3. Navigate to the table **license** in **sqlite_metadata** schema.

3.1 Before doing any other step export the table for backup!

4. Delete the contents of the table (license_file, additional_data).

5. Take the license file you got from our sell team and open it with a txt editor.

5.1 Use the next SQL command:

INSERT INTO license (additional_data,license_file) VALUES("Value1*,Value2*")


Value1: In the license file the first value is the string untill the ******

Example: ![image.png](/.attachments/image-04e8b65d-3a37-4237-982b-6de806fdd6df.png)

Value2: In the license file the second value is the xml like syntax.

Example: ![image.png](/.attachments/image-916b908b-0f98-41dd-9f30-961ab53fe5e7.png)
