# **About**  

The incident dashboard consists of nine plugins, displayed as widgets in the dashboard:
1. Day of Week by Hour
2. Incident Statistics
3. Incident Type Distribution
4. Common Phrases
5. Divisions Activity
6. Incidents by Day
7. Incidents by Hour
8. Incidents Map
9. Involved Entities

# **Configuration** 
Each plugin has its config file called _appsettings.Production.json_, located inside a directory with the plugin's name. e.g., incident_dashboard_plugins/enevtsstatistics/appsettings.Production.json.
Notice two properties of that config file:
- SolrEventsConnectionId- connection to the Events core in SolrDB
- EventsDataModelId- The Schema ID for the Events Data Model. By default, it is -3.

In addition, four other config files manage the properties and deployment of the plugins:
1. _env.local.properties_- Defines the connection to the TA9 repo, and environment variables.
2. _env.system.properties_- controls the image versions of the plugins.
3. _plugins.env_- Env file for image names.
4. _docker-compose_yml_- A standard docker-compose file, that defines configs, secrets, networks, etc.

Make sure that every file is configured properly.

#**Database Configuration**
**Relevant Tables:**
1. _sqlite_metadata.dsb_dashboard_definitions_- Contains ID column whose value should match the Incident Dashboard ID. In the Layout column, there is a JSON file that determines all the widgets' properties; Name, Schema ID, skin, etc.
2. _sqlite_metadata.dsb_dashboard_widgets_ Must contain a row for each plugin. In addition to that, each plugin must have a unique ID and a unique widget ID. WidgetTypeID should equal 1.
3. _dataschemfields1_- Controls the Data Model column settings. Must be configured correctly for the dashboard widgets to function properly- FieldRole, GroupName, and DataEnrichmentName columns should be defined according to the values we'll provide.

#**Deployment**

To deploy the plugins, simply run the _deploy.sh_ script from the stacks directory:
_./deploy.sh -f incident_dashboard_plugins -s plugins_

Ensure that the plugins are up and running by executing:
_docker service ps <service name>_



