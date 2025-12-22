This manual will try to help you start your java development.

1. Install IntelliJ: https://www.jetbrains.com/idea/

2. Get license (TA9 - license)

3. You need to add TA9 repositories located in the Azure:
3.1 Check if you have access to the repositories: https://dev.azure.com/ta-9/Argus/_artifacts/feed/maven, choose 'Maven' in the checkbox (**You should see the artifacts**)
3.2 Go to **Personal access tokens** 
![Personal Access Tokens.jpg](/.attachments/Personal%20Access%20Tokens-34cebed7-7194-4d89-8d50-d9130f3e2c3d.jpg)
3.3 Create new token: Any name, Full Access, set farthest date![Screenshot 2024-01-23 173556.png](/.attachments/Screenshot%202024-01-23%20173556-528b7d27-2d3b-42bc-9945-641418007c6f.png)
3.4 Copy your token. 
![Screenshot 2024-01-23 173836.png](/.attachments/Screenshot%202024-01-23%20173836-9d45bee7-d824-4f21-a944-0cf784cf0f97.png)
3.5 Add token to the password field in [settings.xml](/.attachments/settings-0ba6db6b-0380-42f5-952b-cdae9a52585c.xml) and save the file to c:\Windows\Users\[USER NAME]\.m2\ folder.
 ![Screenshot 2024-01-23 155311.png](/.attachments/Screenshot%202024-01-23%20155311-462ff1c4-3d43-41c9-8b61-9c4d883daad1.png)

4. Go to Bitbucket projects: https://bitbucket.org/ta-9/workspace/projects/ (**Permission from TA9**)

5. All repositories in Backend java![Screenshot 2024-01-23 223503.png](/.attachments/Screenshot%202024-01-23%20223503-51f3bbb2-1e7a-4493-afaa-1dfd5b5375ea.png) ![Screenshot 2024-01-23 223744.png](/.attachments/Screenshot%202024-01-23%20223744-3331159d-d958-4166-9232-c1a1cb8d87ac.png)

6. Follow the sequence of clone and maven operation:

7. Projects with **SDK java 8**
7.1 **Clone and Maven Install** git clone https://david_ilous@bitbucket.org/ta-9/be-java-lib-datacontract.git
7.2 **Clone and Maven Install** git clone https://david_ilous@bitbucket.org/ta-9/be-java-lib-utils.git
7.3 **Clone and Maven Package** git clone https://david_ilous@bitbucket.org/ta-9/be-java-service-indexing.git
7.4 **Clone and Maven Package** git clone https://david_ilous@bitbucket.org/ta-9/be-java-parent-pom.git 
7.5 **Clone and Maven Package** git clone https://david_ilous@bitbucket.org/ta-9/be-java-service-entities.git
7.6 **Clone and Maven Package** git clone https://david_ilous@bitbucket.org/ta-9/be-java-service-report-generator.git
7.7 **Clone and Maven Package** git clone https://david_ilous@bitbucket.org/ta-9/be-java-service-media-analyzing.git
8. Projects with **SDK java 11**
8.1 **Clone and Maven Package** git clone https://david_ilous@bitbucket.org/ta-9/be-java-service-feathered-search.git
8.2 **Clone and Maven Package** git clone https://david_ilous@bitbucket.org/ta-9/be-java-service-text-analytics.git
8.3 **Clone and Maven Package** git clone https://david_ilous@bitbucket.org/ta-9/be-java-service-loader.git

