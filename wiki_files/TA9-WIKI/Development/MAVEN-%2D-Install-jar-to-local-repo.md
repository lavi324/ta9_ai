open command line with elevated permission and execute:
 `install:install-file -Dfile=<path-to-file> -DgroupId=<group-id> -DartifactId=<artifact-id> -Dversion=<version> -Dpackaging=<packaging>`
Use the following parameters:
`<path-to-file>` : the path to the jar to be installed (e.g `c:\artifacts\facerec\test.jar`)
`<group-id>` : com.ta9
`<artifact-id>` : name of the artifact (e.g `FaceRecExternalImp`)
`<version>` : the version of the artifact (mostly used as `0.0.1-SNAPSHOT`)
`<packaging>` : jar

The installed jar will be available to as a maven dependency (within the local machine) in the following manner:

```
<dependency>
   <groupId><group-id></groupId>
   <artifactId><artifact-id></artifactId>
   <version><version></version>
</dependency>
```
