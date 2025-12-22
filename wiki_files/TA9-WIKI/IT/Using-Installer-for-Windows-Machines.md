## Intro
When installing on windows machines, an MSI installer should be used for the following components (one or more, selective):
- System Components:
  - C# Core Services
  - Admin Studio
  - WildFly Services
  - Indexing Service
  - Loader Service
  - Web Client
- Repositories:
  - File Server
  - OrientDB
  - Solr
  - MySQL


The installer creates relevant services on windows server, deploy all artifacts to relevant paths (eg - `Program Files/TA9/...`).
The Files that are copied (artifacts) should be updated to the desired version required before installing.

## Usage Procedure
1. Installer files are located on `\\10.100.102.13\share\Artifactory\Installer\AdvancedInstallerSolution\TA9 Installer`
1. The main entry point is `TA9 Setup.exe`. It is using files from other files/directories (such as `.NET Framework/JAVA SE/etc.`)
1. `TA9 Setup-FILES.7z` is the archive containing all the components mentioned above (except MySQL). 
3.1. Update it to whats needed before using the installer 
3.2. Use files from Artifatory (after building)
1. Copy the whole directory content to the target windows server and run the MSI (`TA9 Setup.exe`)
1. Choose during installation the components you would like to install
1. After installation is finished - perform additional configurations according to installation-document


## Installer Modifications
We're using [Advanced Installer](https://www.advancedinstaller.com/) licensed product in order to create our installation packages.
* If there's no a special reason (such as an additional component/bug), **the installer should not be changed**, but only the files that's being used by it (as listed above).
### Method
1. Advanced Installer should be installed from here: `\\10.100.102.13\share\Artifactory\Installer\advinst.msi` 
1. Installer solution is located here: `\\10.100.102.13\share\Artifactory\Installer\AdvancedInstallerSolution`











