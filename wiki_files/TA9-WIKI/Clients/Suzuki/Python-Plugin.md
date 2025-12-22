#Introduction
In this tutorial, we will understand how to create a plugin to execute a specific python script.

#Setup
In order to run python through .Net, we need:
1. To have python (We use V2.7) installed on the local machine and create a process (ProcessStartInfo) and give it the script as an input.
2. To install IronPython which can be acquired through NuGet and it is a python implementation in .Net.
   - IronPython's version is the python version itself - meaning that in order to work with IronPython we need to make sure that the IDE we write/provide the python script is the same/lower as IronPython's version.
   - As we know python is working well with a lot of libraries. We will need to provide the location of the lib folder for the plugin to be able to run the scripts (e.g. "import JSON" etc).
![pyhton1.PNG](/.attachments/pyhton1-c35b7b37-4dc8-4507-8e3c-fce09ebbe184.PNG)

3. We will also provide the script itself path.
![python2.PNG](/.attachments/python2-5cf30ff7-0a82-4ea3-bfb6-2c30ad0a0786.PNG)

#Flow
![pyhton3.PNG](/.attachments/pyhton3-97831af4-9bef-4f6c-909e-a4f4d863a749.PNG)

Line 33-37 - getting a parameter for later use.

Line 38 - Reading the script as a string because the engine takes a string only.

Line 40 - Actually the "python.exe" of IronPython.

Line 41-43 - Here we give the engine the relevant path - otherwise it won't know how to use the "import" libraries inside the script, like a "using" statement without a reference.

Line 46 - In order to run the script and get results back we provide a scope for it to run.

Line 47 - Here we run the script in the scope we created.

Line 50 - In our scope, there is our script and we look for a function that is called "getData" - exactly as the function name provided in the python script itself we read in line 38.

Line 51 - Here we get the result after the function finished executing.
"var result" is a dynamic type. Note that we send a parameter because the python script function takes exactly 1 parameter.

After that, the manipulation of "result" is just like a normal plugin handling.






