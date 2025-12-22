1. Create a maven project (simple==jar)
2. Add dependency to face-rec-contracts (make sure it's installed in machine. see [howto](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/64/MAVEN-Install-jar-to-local-repo))
3. Implement the interface you wish (eg - `IDetectionManagement`)
4. When you're ready, maven->install
5. Goto to "target" and grab the created jar file
6. Place it in an accessible location by the wildfly
7. Goto config table and set following keys:
7.1. `FaceRecognitionDetectionManagment` ==> "External"
7.2. `EXTERNAL_JAR_FACE_RECOGNITION_DETECTION_MANAGEMENT` ==> Full absolute path of the jar, preced by "file" protocol and double regular slashes (e.g "`file:///C://git2//utils//PluginSamples//target//pluginSamples-1.0-SNAPSHOT.jar`")
7.3. `EXTERNAL_CLASS_FACE_RECOGNITION_DETECTION_MANAGEMENT` ==> full qualified name of the class that implements the interface (e.g "`com.ta9.pluginsamples.facerec.FaceRecDetectionsProvider`")
8. Restart `FaceRecognition` service


**KNOWN ISSUE:** If using other classes on the implementing class, you must also put the JAR in the WAR that's dynamically-loading it. on: /WEB-INF/lib/
See #39331
