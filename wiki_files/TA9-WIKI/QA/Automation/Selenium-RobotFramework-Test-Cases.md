[[_TOC_]]
# **RobotFramework**

[Robot Framework](https://robotframework.org/) is a generic open-source automation framework.

 

It can be extended by libraries implemented with Python, JavaScript and many other programming languages.  

#**Selenium & Important Libraries**

RobotFramework is supported by many libraries which offer functions and interfaces 

 that make the automation developing much easier, some of the most important 

 The libraries are: 

- **SelenuimLibrary**

  [SeleniumLibrary](https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html) is a UI web testing library for Robot Framework. 

  By using Selenium WebDriver modules it’s possible to control the web browser with simple commands.  

- **String**

  A [library](https://robotframework.org/robotframework/latest/libraries/String.html) for string manipulation and verification.  

- **DateTime**

  A [library](https://robotframework.org/robotframework/latest/libraries/DateTime.html) for handling and converting date and time values.


- **OperatingSystem**

  A [test library](https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html) provides keywords for OS-related tasks. 

- **Collections**

  A [test library](https://robotframework.org/robotframework/latest/libraries/Collections.html) provides keywords for handling lists and dictionaries. 

- **RPA.Word.Application**

  Library for controlling a Word application.

And of course, there are many more. 

---

#**Our Automation Process:**

- Every single feature has it own **Test Suit** 

- **Test Suits** built from several **Test Cases**

- Each **Test Case** is responsible for checking a specific part or functionality of the main feature. 

![Picture13.png](/.attachments/Picture13-a3b0831b-6a50-4b2b-8503-9eef81eef1c3.png)

The test cases are first written for the manual testing process, 

and then we base our UI automation on these tests. 

We also would like to validate that the test instructions are up to date and match the current

version/system requirements specification. 

Every test case is divided into several steps that guide the automation engineer with its writing process: 


![Picture14.png](/.attachments/Picture14-005ef225-6ea3-4b86-806b-5e25263f95cf.png)
       _screenshot from Azure-Devops that describes the test case structure_

---

# **HTML Selectors**

**To perform actions in the web browser, first, we need to select the elements we are going to work**

 **with.**

We indicate the webdriver about the wanted elements using selectors, the webdriver is filtering the HTML

page according to the selectors that defined to it. 

By that we can perform necessary actions such as clicking elements, writing text into them etc. 

In our automation code, we usually use XPath and CSS to set selectors for elements, 

 although it is possible and sometimes even better to define other types of selectors  

(For example, by the element id). 

[Click Here](https://www.w3schools.com/cssref/css_selectors.php) for tutorials on **CSS** selectors 

[Click Here](https://devhints.io/xpath) for tutorials on **XPath** selectors 



# **Selectors Using:**

On login page, using this XPath selector: 

**//button[contains(text(), "SIGN IN")]**

will allow us to select the “Sign In Button” and perform actions with it such as hovering the mouse upon it,

clicking, check visibility etc. 



![Picture15.png](/.attachments/Picture15-61b53118-45eb-469d-a9f8-d127a2787c78.png)



Let's start with a code example: 

```
import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace() 
 
*** Settings *** 
Library  chrome_driver.py 
Library  pyperclip 
Library  selenium 
Library  Selenium2Library 
Library  OperatingSystem 
Library  DebugLibrary 
Library  DateTime 
Library  String 
Library  RPA.Word.Application 
Library    Collections 
 
 
*** Variables *** 
${URL}      http://10.100.102.50/ng/login 
${BROWSER}  Chrome 
${User_Name}    Ori_Admin 
${Password}    jkp@_y7ahg 
${User_Name_Field}    css=#mat-input-0 
${Password_Field}    css=#mat-input-1 
${Login_Button}     xpath=//button[contains(text(), "SIGN IN")] 
${Portal_Page}    http://10.100.102.50/ng/portal 
${Add_Case_Button}  xpath=//*[@class="p-element cursor-pointer hover-opacity add-icon ng-star-inserted"] 
${Case_Name_Field}  xpath=(//input[@class="dx-texteditor-input"])[1] 
${Save_Button}      xpath=//button//span[text()="Save"] 
${Success_Toast_Message}    xpath=//div[@class="toast-title" and text()="Case was saved successfully"] 
${sidebar_user_button}   xpath=/html/body/div[1]/div/div[1]/header/ht-top-nav/div/div[1]/div 
${sidebar_user_button_logout}    xpath=/html/body/div[1]/div/div[1]/header/ht-top-nav/div/div[2]/div[1]/div
```



- First, we can notice the **Settings** section. 

  It is usually used to import libraries and extensions for RobotFramework that contain functions,

   variables etc. 



- After the Settings section, we have the **Variables** section. 

  It contains the variables we want to set up before runtime,

  for example: Login credentials, URLs, XPath/CSS selectors etc. 



```
*** Keywords *** 
Login 
    [Arguments]     ${login_name}    ${password} 
    ${driver_path}=    get_chromedriver_path 
    Open Browser    ${URL}    ${BROWSER}    executable_path=${driver_path} 
    Go to    ${URL} 
    wait until location is    ${URL} 
    Maximize Browser Window 
    Wait Until Keyword Succeeds    1 min    1 sec    Element Should Be Visible    ${User_Name_Field} 
    input text    ${User_Name_Field}    ${login_name} 
   input text    ${Password_Field}    ${password} 
   click button    ${Login_Button} 
   wait until location is    ${Portal_Page} 
 
Logout 
    Wait Until Keyword Succeeds    1 min    1 sec    Element Should Be Visible     ${sidebar_user_button} 
    click element    ${sidebar_user_button} 
    Wait Until Keyword Succeeds    1 min    1 sec    Element Should Be Visible     ${sidebar_user_button_logout} 
    click element    ${sidebar_user_button_logout} 
    Sleep    5 sec 
    Wait Until Location Is    ${URL} 
    Wait Until Keyword Succeeds    1 min    1 sec    Element Should Be Visible    ${User_Name_Field} 
 
 
*** Test Cases *** 
Create a new case 
    Login    login_name=${User_Name}    password=${Password} 
    Wait Until Keyword Succeeds    1 min    1 sec    Element Should Be Visible    ${Add_Case_Button} 
    Sleep    3 sec 
    Click Element    ${Add_Case_Button} 
    Sleep    5 sec 
    Switch Window   New Case 
    Wait Until Keyword Succeeds    1 min    1 sec    Element Should Be Visible    ${Case_Name_Field} 
    Input Text    ${Case_Name_Field}    MyNewCase 
    Sleep    2 sec 
    Click Element    ${Save_Button} 
    Wait Until Keyword Succeeds    1 min    1 sec    Element Should Be Visible    ${Success_Toast_Message} 
    Logout 
    Close Browser 
```



  After we defined everything that’s necessary, it’s time to start doing some automation!



- First, we’ll look at the **Keywords** section. 

  Under this section we write our Shared Steps - an action that is built from a 

  group of steps, that repeat itself in several cases that is not related directly to a 

  specific test case. 

  The shared steps are basically functions, and can receive parameters, 

  for example: Login Keyword gets a login name and a password. 



- After we defined the keywords, we start to write our **Test Cases** section. 

  In this scope, we implement our written test cases from the Azure-DevOps into 

   Code. 







Most of the time, automation tests contain more verifications and inner tests 

than specified in the test case instructions in Azure-DevOps. 

These tests are used to validate details that seem obvious to the manual testers 

like: Checking the visibility of images or texts, validating that we are directed to 

the wanted URL, make sure that uploaded data is really added and stored in our 	DB, etc. 




**The tests run sequentially by the order they are written.**

**Because of that, we should never forget to close our browser/application after every run of** 

**automated test case.** 

**When all the tests running finished, RobotFramework will display the tests results in the terminal:**




![Picture16.png](/.attachments/Picture16-9dafbca9-07c8-471d-8b27-156c64506341.png)

#Passing Test Cases

When test case is passed, it can be caused by two reasons: 


- The software works as intended and passed the test. 



- Our test doesn’t check and validate all the system behaviors and actions as it 

  should. It may cause a situation where a test is passed although it should have 

  failed. 

# Failing test cases 

Like passed test cases, failed tests can also be caused because of two reasons: 



- The software doesn’t work as it should according to the test case instructions. 

 

- Our automation accidentally tests or waits for certain behaviors/values that shouldn’t exist. 




**Notice**: To avoid the incorrect cases described, when we run the automation during development, we will 

always watch its running process. 




**If a test case automation is successfully passed – Congratulations!** 

**If it failed and we understood clearly that it is caused because of a bug or exception,**  

**we would like to notify the QA team lead and open a bug if it’s necessary.** 



---


# **Common Errors/Problems**


**Element is visible but isn’t recognized by the WebDriver** 

This problem can be caused by several reasons: 



- The element’s selector isn’t specific enough and may be related to more than one element. 

  In this case, try to expand the selector definition that will include only the wanted element. 



- The element appears at the bottom of the page, and it is necessary to scroll to it. 

  To perform this action use:   ```Scroll Into View 		${Wanted_Element}``` 



- The element you’re looking for placed in other iframe. 

  In this scenario, try to find the other iframe’s id and then selecting it by: 

  `Select Frame	id:example-iframe`



![Picture17.png](/.attachments/Picture17-515cee37-2d83-4265-ad9a-0d09baa9edac.png)
_Screenshot from DataModel – all the elements in this area are included under criteria-iframe_




**Elements exist but aren’t visible because of screen resolution:**

To fix this, you can use: 

```
${Width}	${Height}=		Get Window Size 

${New_Width}=	Evaluate	${Width} - 50 

${New_Height}=	Evaluate	${Height} - 50 

Set Window Size 		height=${New_Height}		width=${New_Width} 
```
