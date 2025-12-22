[[_TOC_]]
# Intro
This plugin is used to get the shortest path with permission validation.

#To install it
Put the JAR file from this project in the orient’s Lib directory.

-In the orientdb-server-config.xml file add command tag inside the <listeners> → <commands> hierarchy, with implementation, pattern and stateful properties.
the implementation property should be the name of the package and project (for example com.ta9.OServerCommandGetShortestPath)
This is the current command config:
<command implementation="com.ta9.OServerCommandGetShortestPath" pattern="GET|shortesPathPlugin/*"/>

# restart orient

## Docker ENV
sudo docker restart orientdb

## Dedicated ENV
sudo systemctl restart orientdb.service

-check for this message when you restart orient to see that the plugin was loaded:

# Log file should return this

"TA9 shortest-path plugin loaded successfully [OServerCommandGetShortestPath]"

---------------------------------------------------------------------

This manual gives example for short implementation like this plugin:

https://gist.github.com/vitorenesduarte/12a47ac37ce9ce5f9506

This is the source code:

https://github.com/orientechnologies/orientdb/blob/2.2.x/graphdb/src/main/java/com/orientechnologies/orient/graph/sql/functions/OSQLFunctionShortestPath.java  

more info in task TA-2342 and in wiki