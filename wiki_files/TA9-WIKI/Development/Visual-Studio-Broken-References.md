Ever came across a million errors while loading a project that was not opened for awhile?
You may need to reinstall packages from NuGet:

Go to:
Tools > Options > NuGet Package Manager. 
Under Package Restore options, select "Allow NuGet to download missing packages" and "Automatically check for missing packages during build in Visual Studio".

While you're at it, clear the cache as well.

![image.png](/.attachments/image-ca4e2696-3e80-4083-a967-058605af59dc.png)

After that, go to the solution, right click it and choose "Restore NuGet Packages:

![image.png](/.attachments/image-bb228f60-819f-4c7b-bb61-182c4a31ffeb.png)

Let it run, and double click any left error, it will open the file and reload the reference again.

