To share and consume common **DLLs**(such as **TaExtensions.DataContract**, **LoggerUtils** and others) we can use **Azure DevOps Artifacts** service.

## Add _Artifacts service_ to Nuget Package Manager in Visual Studio
If you want automatically connect to **Artifacts service** in Visual Studio follow these steps:
1. Open **Visual Studio** and click on **Continue without code**
![image.png](/.attachments/image-4bf9afc1-c3d7-4963-b0f5-6532e7b4094c.png)
2. Open Package Manager Settings : **Tools > NuGet Package Manager > Package Manager Settings** 
3. In **Package Sources** tab add new online Package source.
- Press **+** to add new Source
- Fill the **Name** field(whatever you want)
- Fill **Source** with following link and click on **Update**
`https://pkgs.dev.azure.com/ta-9/_packaging/Main/nuget/v3/index.json`
4. In Nuget Package manager you can [switch](#add-offline-nuget-package-to-new-project) between **nuget.org** and your sources.

## Another way to connect to Feed and consume packages
With Azure Artifacts, you can publish your Nuget packages to public or private feeds, and then share them with others, depending on your feed's visibility settings. 
_In TA9 I assume we will use **"Main"** feed for Nuget packages._

1. From Argus project in Azure DevOps, select **[Artifacts](https://dev.azure.com/ta-9/Argus/_packaging?_a=feed&feed=Main)**, and then select **"Main"** feed if not selected.
2. Press **Connect to feed** and then press on **NuGet.Exe**.
3. Follow official instructions in opened window.

nuget.config creation:
![image.png](/.attachments/image-87518198-422d-46f5-ad5e-cdc23ff75b70.png)
nuget.exe restore:
![image.png](/.attachments/image-73401376-a07e-44fd-8060-0db602573037.png)

## Add Offline Nuget package to new Project
1. Go to TA9 Argus [Artifacts](https://dev.azure.com/ta-9/Argus/_packaging?_a=feed&feed=Main) 
2. Find required package and download it.
3. In Visual Studio open **Tools > Nuget Package Manager > Package Manager Settings**
4. In **Package Sources** tab add new offline Package source.
- Press +.
- Choose Source: folder 
![image.png](/.attachments/image-a075d818-6c92-44cc-9f91-d6fc5dd0c23a.png)
5. Put downloaded package to created offline source folder.
6. To switch between sources in Visual Studio, **right-click the project in Solution Explorer > Manage Nuget Packages > change Package source on the right to your Offline source**.
![image.png](/.attachments/image-af526950-13b4-470a-974c-b527baa761bf.png)
7. Install needed Nuget package.


## Create and Publish packages
1. To create new Nuget package for .Net Framework class library follow official [instructions](https://docs.microsoft.com/en-us/nuget/quickstart/create-and-publish-a-package-using-visual-studio-net-framework) 

![image.png](/.attachments/image-64a7eaa3-b14f-43fb-a7da-9aa2204252bc.png)
### nuspec file example
```
<?xml version="1.0" encoding="utf-8"?>
<package >
	<metadata>
		<id>$id$</id>
		<version>3.9</version>
		<title>$title$</title>
		<authors>TA9</authors>
		<requireLicenseAcceptance>false</requireLicenseAcceptance>
		<license type="expression">MIT</license>
		<!-- <icon>icon.png</icon> -->
		<description>TA9 metadata data contract</description>
		<releaseNotes>Updated to 3.9 version.</releaseNotes>
		<copyright>$copyright$</copyright>
		<tags>Metadata</tags>
		<dependencies>
			<dependency id="UserManagement.DataContract" version="1.0.0" />
			<dependency id="TaContracts.Common" version="1.0.0" />
			<dependency id="Utils.Attributes" version="1.0.0" />
			<dependency id="Newtonsoft.Json" version="12.0.3" />
		</dependencies>
	</metadata>
</package>
```

![image.png](/.attachments/image-ab09aa0f-df4f-4547-afbc-76a8a33e640b.png)

   To Create new Nuget package for .Net Core class library follow official [instructions](https://docs.microsoft.com/en-us/nuget/quickstart/create-and-publish-a-package-using-visual-studio?tabs=netcore-cli) 

2. Publish a package by providing the package path, an API Key (any string will do), and the feed URL :

   `nuget.exe push -Source "Main" -ApiKey az <packagePath>`

![image.png](/.attachments/image-4b72b176-e462-4277-b951-4a9691976f3a.png)

![image.png](/.attachments/image-a1432ebe-87bb-4c0a-8c93-02869ccfe27e.png)