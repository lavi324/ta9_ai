If you try to compile and get an error like this:
"Your project does not reference ".NETFramework,Version=v4.6.1" framework. Add a reference to ".NETFramework,Version=v4.6.1" in the "TargetFrameworks" property of your project file and then re-run NuGet restore."

You need to do the following steps, because "clean" is not enough:

1. Clean the project.
2. Navigate to the projects' main folder and locate the "obj" folder in each of the sub-projects.

![image.png](/.attachments/image-7df175fe-b94d-4e34-af27-ff38ac2d6ac0.png)

![image.png](/.attachments/image-79075a1d-11e8-4717-b594-16fb781f934b.png)

![image.png](/.attachments/image-c56a92c2-16a2-4dba-8bc0-f59eef257073.png)

3. Delete the "obj" folders.

4. Go back to the solution and re-run NuGet restore.

![image.png](/.attachments/image-f4d18b05-0f88-4eff-a3b0-529ac9224e63.png)

5. Build the project again. It should be fine.