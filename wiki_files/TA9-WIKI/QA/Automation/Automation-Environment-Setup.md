In order to setup the automation environment you will need to execute the following steps

[[_TOC_]]

# 1. Install Python

Navigate to https://www.python.org/downloads/release/python-390/ 

Download the “Windows x86-64 executable installer” file 

Execute the file to install Python 3.9. Copy the full folder path in which you are installing Python (You will need it for later)

![image001.png](/.attachments/image001-781e8c4b-049d-4542-aa13-c159bd88fdb3.png)

Search for “Environment Variables” in the windows search

Click on “Edit the system environment variables”

![image003.png](/.attachments/image003-581d804e-5e9e-4cdd-a3bf-b0a98c6083bb.png)

Click on “Environment Variables...”

![image005.png](/.attachments/image005-ec3b623e-20ed-4ae1-a186-d850b96136e7.png)

Click on “Path” and then click on "Edit"

![image006.png](/.attachments/image006-26cb47a7-4675-468f-aff9-a5c0db2278ea.png)

Add a new path by clicking on “New”

![image008.png](/.attachments/image008-4923387f-fe06-41e1-8246-25fff5ab5d1c.png)

Enter the Python folder path and click on “OK”

![image.png](/.attachments/image-002e66fd-66e7-40b7-b76b-d150f820cf4d.png)

# 2. Install PyCharm Community IDE

Navigate to: https://www.jetbrains.com/pycharm/download/#section=windows

Install the latest version of "PyCharm Community"

# 3. Install Robot Framework Libraries

First, make sure that [pip](https://pip.pypa.io/en/stable/installation/) is installed

Then, Use pip in the PyCharm console to install all [relevant libraries](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/739/Selenium-RobotFramework-Test-Cases)

- Install the main Robot Framework library

```
pip install robotframework
```

- Install SeleniumLibrary for Robot Framework

```
pip install --upgrade robotframework-seleniumlibrary
```

Note: You can also install the libraries via the package manager in PyCharm
![image.png](/.attachments/image-ad1a82f3-b763-43b9-a54f-115757184c13.png)

# 4. Setup Selenium WebDrivers

For Chrome install -

Open the Chrome browser, enter “chrome://settings/help” in the address bar
Note the Chrome browser version (97.0.46 for example)

![image012.png](/.attachments/image012-2e7260c5-50dd-48f3-b932-5bf67bf3f3bf.png)

Find the matching Chrome driver version in the following URL: https://chromedriver.storage.googleapis.com/index.html

![image014.png](/.attachments/image014-1c28e4e8-9413-48d2-97ad-5ee7a2d8b950.png)

Download the “chromedriver_win32” zip file (note that all the other files are not for Windows)

![image016.png](/.attachments/image016-148fc300-95e9-4826-8b5f-e082e50ac102.png)

Extract the “chromedriver.exe” to a dedicated folder in your pc

Note: You can also use the [WebdriverManager](https://github.com/MarketSquare/webdrivermanager) tool to automatically download the driver
You can see the usage in the file 'chrome_driver.py' in the Automation repository

# 5. Install Robot Framework Plugin

You need the plugin for -
- Syntax Highlighting
- Code Completion
- Keyword Navigation

You can use any plugin -

- [Hyper RobotFramework Support](https://plugins.jetbrains.com/plugin/16382-hyper-robotframework-support)
- [Robot Framework Support](https://plugins.jetbrains.com/plugin/7415-robot-framework-support)
- [RobotFramework Helper](https://plugins.jetbrains.com/plugin/21066-robotframework-helper)

# 6. Install Git

Navigate to https://git-scm.com/download/win, download and install the “64-bit Git for Windows Setup”

# 7. Connect Azure DevOps to PyCharm

Click on File -> Settings. In the settings window, navigate to the “Plugins” tab and search for the “Azure DevOps” plugin. Install the plugin by clicking on “install”. Click on “OK”.

![image018.png](/.attachments/image018-d46ba139-940e-4ab9-85df-1b21f32e34a9.png)

# 8. Clone the automation repository 

Click on “VCS” and then choose “Get from version control...”

![image020.png](/.attachments/image020-96365639-5bfc-472f-9234-da96fa4c914d.png)

In the "Repository URL” tab, under the “Version Control” field, choose “Azure DevOps Git”

![image022.png](/.attachments/image022-734df1d5-31a9-4c16-95ac-7c3e5d210085.png)

Click on “Clone”

![image024.png](/.attachments/image024-e98aecc3-d62f-4a66-b912-a16578d662dc.png)

Sign in to Azure DevOps with your credentials

![image026.png](/.attachments/image026-6a5f90f1-1acd-4cd9-b72b-f1de5faac965.png)

Choose the “AutomationPython” repository and enter the folder (Parent directory) in which you want to clone to project into
Then click on the “Clone” button on the bottom right

![image028.png](/.attachments/image028-95811965-89c9-403c-8d1e-0702d0c8dbb3.png)

After the code has finished cloning, click on the bottom right to checkout to the branch that you need.

![image030.png](/.attachments/image030-a91886ff-8f63-4ab6-bccd-32b1de91815c.png)


# 9. Install Allure Report - Not relevant For Now

~~Download the latest version of the zip from this [URL](https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/)~~
~~Unpack the content of the zip to a dedicated folder.~~
~~Navigate to the bin folder in the extracted folder.~~
~~Click on “allure.bat” to run it.~~
~~Open the “Environment Variables” in Windows, and add “allure” to the system “PATH” (Just as you did with Python)~~

~~Open the command prompt in Windows and run the following command “allure --version”.~~
~~If the installation succeeded, you will see the allure version number.~~


![image031.png](/.attachments/image031-dbadbd17-a20f-4650-82c8-71159965c93b.png)


# 10. Import relevant Python libraries (Only If needed)

Install the libraries from the code files by importing them from the code itself by clicking on “install package `library name`”

![image032.png](/.attachments/image032-290d7492-a1f6-4b55-99bf-5e971d9ae609.png)