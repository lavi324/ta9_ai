
[[_TOC_]]

# **Postman:** 

Postman is an API Platform for developers to design, build, test and iterate their APIs. 

Learn more about Postman at:  https://www.postman.com 

# **API Testing**: 

API testing is a type of software testing where application programming interfaces (APIs) are tested to determine if they meet expectations for functionality, reliability, performance, and security. 

Using the API, we’re being revealed to new options that aren’t offered to us in the UI. 

[Click Here](http://10.100.102.23/swagger/index.html) for our API Swagger Documentation 

# **Environments & Collections** 

- Collection – A group of API requests that are saved together.

  The requests in a collection are ordered by their sending sequence. 

  The collection enables running all the requests together by their order. 

  Collections can also store in their scope values and variables that 

  related to its purpose and can be used and edited during runtime. 


- Environment – A data scope that can be defined by the user and 

  can be applied to any requests or collections before and during running. 

# **Requests Structure**
There are several fields and values that HTTP request is built from:

- **URL:** The web address of the service or resource we would like to work with

- **Method:** The type of operation we would like to perform. 

  For example:

  GET (to ask for certain data or resource),  

  POST (most of the time used for adding or uploading data), 

  PATCH (modifying certain part of resource), 

  PUT (modifying that will affect the whole resource), 

  DELETE (Deleting data), etc. 


   ![Picture1.png](/.attachments/Picture1-51c11ab7-12c1-4db7-882f-a1cd03d9bba9.png)
_Postman screenshot- Method from the left, URL from the right. BaseURL is an Environmental variable._ 




- **Payload**: The body of the request, most of the time contains data we want to 

  send, or details about what we want to get from the system. 

  **Notice that some requests can contain no payload.** 

![Picture2.png](/.attachments/Picture2-bdc8ccfe-27e9-43a8-a438-eaf487308f12.png)
_Postman screenshot- Method from the left, URL from the right. BaseURL is an Environmental variable._ 


- **Headers**: Fields related to the request’s format and attributes (For example – 

  Content-Length). 

  Most of those fields are automatically defined by Postman. 

![Picture3.png](/.attachments/Picture3-5096f5a0-fcf4-4849-b84f-e3f38116f397.png)
_Postman screenshot – The request’s default headers_ 


 - **Parameters**: These parameters can be added to the request’s URL. 

    There are two optional types of parameters: 

    -  **Path Parameters**: Most of the time are used to “navigate” through services’ resources. 

        In postman to add a path parameter we use ‘:’ and the parameter 		name right after it:

 ![Picture4.png](/.attachments/Picture4-c05d16ec-286d-43a1-bb47-f52a75f8da80.png)
_Postman screenshot – In this example, we use a path parameter as entity_id_ 



   **Query Parameters**: Parameters that are used as a part of a query (for 

  example – filtering data by certain attributes). 

Query parameters declared by the character ‘?’ and the parameters name right after: 

![Picture5.png](/.attachments/Picture5-0f512229-1ab6-4a0b-a93e-0ba7e929257d.png)
_Postman screenshot – In this example, we see the usage of query parameters to filtering tasks into a list_ 
 
- **Authorization**: 

  Before almost every API call, we will need authorization. 

  We perform the authorization through the Login API call: 

![Picture6.png](/.attachments/Picture6-e55fdfd9-2d23-4585-b9f6-717537e85757.png)

After every successful login, we get in the response **Login Token**. 

Using the following code, we take the Login Token from the response and save it 

into variable in the collection’s scope: 

```
var jsonData; 

pm.test("Response status check", function() 

{ 

    pm.response.to.have.status(200); 

    jsonData = pm.response.json(); 

    if (jsonData.code != 200) 

    { 

    	pm.expect.fail("Invalid response message");   

    } 

    var loginToken = jsonData.data.LoginToken; 

    var userID = jsonData.data.UserID; 

    pm.collectionVariables.set("UserID", userID); 

    pm.collectionVariables.set("LoginToken", loginToken); //save login token for authorization in the next requests 

}); 
```

Then in the next requests we will have to use this token for authorizing: 

In 3.9 we will set the token in the request’s headers: 

![Picture7.png](/.attachments/Picture7-b5cf2a0d-a0df-463f-a3f3-011e24ae0473.png)

In 4.0 we will use the **Authorization** tab, and in Type we will select Bearer Token: 

![Picture8.png](/.attachments/Picture8-bfb3a510-ac5e-4a38-8d2a-d9810151568b.png)

**Notice: every Login Token has an expiration time (that is sent with the token in the login response).**
**After the token is expired, you will be asked to log in again, or you will get “401 Error – Unauthorized"** 

As a part of the request creation, we usually use the UI on the web to learn about the 

request we are adding to our collection: 

![Picture9.png](/.attachments/Picture9-04d0a2f9-5f51-4084-addd-acd5325059e8.png)

Using the browser DevTools, we can look at the API calls that are sent to the services 

and compare important fields such as: 

- **URL** 

- **Method** 

- **Payload** 

- **Excepted Response** 

- **Tokens** 

- **Headers** 

It all helps us understand the successful operation of the API calls and validate that we are using them 

correctly in Postman. 

# **Tests**
The tests section enables us to automate the testing on the API requests. 

For every request, we write in JavaScript the code using postman’s frameworks “**PM**” 

 and “**Postman**”. 

In the testing section, we can also have access to the system response content, 

and by that, perform essential actions. For example – store data into values, create 

 Conditions and save important tokens: 

![Picture10.png](/.attachments/Picture10-7245daef-68e9-4a65-8f6d-5d8a1fbe8491.png)
_Postman screenshot – In this example we see an Entity Creating Request._ 
 _The test that validates that the response status code is equal to 200._ _If the test passes, it will save the returned entity id into variable in the collection’s scope_ 

**Notice**: In cases of adding or modifying data, we also would like to check if the rows that should have been changed or added in the DB are actually updated (Using the MySQL tables or the OrientDB). 

# **Export/Import an Existing Collection** 

After we finished working on a collection, it is possible to export and sharing it: 

![Picture11.png](/.attachments/Picture11-26b1f6b0-4f62-4e15-9baa-be18df35f000.png)

- First, navigate to Collections. 

 

- Then hover with the mouse on your collection and click on the 3 dots menu or right click the collection’s tab. 

 

- Choose Export in the options menu. 

 

- Select the wanted version and then click on Export and download the file. 

 

**The file will be saved in an MyCollectionName.postman_collection.json format.** 


If you would like to import an existing collection, follow these steps:  

![Picture12.png](/.attachments/Picture12-cb314242-2295-4edc-b42b-c250821e6b20.png)

- Click on Import at the top of the window. 

 

- Now you can browse in your file manager to the collection file or just drag and drop it. 

 

**Notice: The imported file must be in the same format as noted in the Exporting Guide.** 