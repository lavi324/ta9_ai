REM plugins, insights, and other code files are going through a Content Disarm & Reconstruction (CDR) process (Halbana) using an OWASP open-source tool to perform a best-effort analysis of 3rd party dependencies in every code file.

OWASP dependency-check-cli is a command-line tool that uses dependency-check-core to detect publicly disclosed vulnerabilities associated with the scanned project dependencies. The tool will generate a report listing the dependency, any identified Common Platform Enumeration (CPE) identifiers, and the associated Common Vulnerability and Exposure (CVE) entries.

In order to use it, follow the following instructions:
[DependencyCheck](https://jeremylong.github.io/DependencyCheck/dependency-check-cli/index.html)

Run the Dependency-Check from the extracted folder using the command:
 `dependency-check.bat --project "My App Name" --scan "C:\Code\Backup\Insight"`

![image.png](/.attachments/image-b12f7140-c802-4251-a7dd-de033de04d89.png)

![image.png](/.attachments/image-dc2adf46-a97e-4ce5-bb22-975d571258a2.png)


The result should be a report such as - 
![image.png](/.attachments/image-de45c14a-f109-42d5-b06b-5a99e5ee36c8.png)

Eventually, you want the report to look like this, with no vulnerabilities at all - 
![image.png](/.attachments/image-98590a58-12b8-4cd0-8ba7-989d375f93d4.png)

