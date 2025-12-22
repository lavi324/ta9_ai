## The following app supports translating the system to a different language.

## App location:
Z:\Artifactory\TA9Tools\T-App

## The Application use-flow and notes.

* Each TA9 version comes with a unique base translation file. 
![image.png](/.attachments/image-58b587b7-426e-4f85-b1d2-62d55c321245.png)

* Please prepare your version-based translation in a separate folder for future use.

* The app will create a new Distinct Values XLS file from the base translation file. The new file will be created in the base translation XLS file folder

* After translating the Distinct Values file, you can upload it to the app, and a script that updates the values will be created in the folder location of the Distinct Values file.

## How to use the app:

* Double-click the TranslationApp.exe
![image.png](/.attachments/image-caa950f6-18d5-4c08-8745-2011d38c0704.png)

* Press on the Select File button and select the base translation file you received in the version release.
![image.png](/.attachments/image-16c95a66-25d2-47e7-9399-d5cd4edc1e26.png)

* Press on the Get Keys button to create the Distinct Values file.
![image.png](/.attachments/image-a5de4291-506f-4555-85a6-4ca4894f657b.png)

* The Distinct Values file will have two columns: Key and Translation. 
Please insert your desired translation for each **Key** in the correspondent **Translation** column. 

![image.png](/.attachments/image-b2243d18-891c-4637-8d24-0621103b5c94.png)

![image.png](/.attachments/image-fe0bdd1d-9321-44ec-a24e-646630ba758a.png)

* When editing the Distinct Values files, you must save the file in CSV UTF-8 format, to support special characters in different languages.

![image.png](/.attachments/image-4add5194-7f8d-4af2-8705-a291b09028f6.png)

* Upload the translated Distinct Values file to get the UPDATE SQL script. After pressing the button **Get script from translation** and selecting the translated Distinct Values file, the script will be created in the folder location of the Distinct Values file.

![image.png](/.attachments/image-e1d1e5a6-2f31-419d-848e-69ea290734b5.png)

* The generated script contains an UPDATE statement that updates the Trans_2 column in sqlite_metadata.language_translation table in the Maria DB. 
* PLEASE NOTE: If you wish to update a different column, please change the script accordingly and change the Trans_2 to your relevant column name (Trans_1, Trans_3, etc.) 
![image.png](/.attachments/image-00bc3ffc-73c0-43df-852e-af066375bc27.png)

**Ignore List txt file.**
* Inside the app folder there is a text file named ignoreList.txt
![image.png](/.attachments/image-63ef1c6d-cb21-416c-ae40-01fb3f9e0c1b.png)
This file contains a list of translation keys the app ignores, to maintain a summarized list of keywords that need to be translated. 
This file must exist in the folder where you run the app.
You should not change the file name or content without consulting the Support Team.