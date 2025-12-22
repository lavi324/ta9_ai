Here is a table that presents a mapping file of all the parameters in "Vault" tool based on the following:

- Parameter Name
- Parameter ID
- Data type (tring/int/etc)
- Data values (tru/fals/etc)
- Default value
- Affecting on


|Parameter Name|Data Type|Default|Affecting On|
|--|--|--|--|
|ActiveDirectory|JSON|{ "AdminGroupName": "{LDAP path to admin group}","ClientUserPropertyName": "", "DepartmentsGroupName": "{Departments group LDAP path}", "IpAddress": "", "Password": "", "Port": ,"SynchronizationInterval": ,"UserGroupName":"{ServiceAdmin group LDAP path}", "UserName": ""}|Will figure to know the AD info, if want to enable go to "ExternalUserManagement" config|
|CacheConfig|JSON|{ "DefaultExpirationTime": "", "DefaultShortExpirationTime": "","GlobalInstance": "","RedisConnection": "{IPADDRESS:6379,password=redis!@#$}","UseHealthCheck": ""}|config of redis - cache DB|
|ConnectionStrings|JSON|{ "DefaultConnection": {"ConnectionString": "server=IPADDRESS;userid=root;password=mysql!@#$;database=sqlite_metadata;Port=3306;CharSet=utf8;", "DBType": "","ProviderName": "MySqlConnector"},"LocalizationResourceFiles": {"ConnectionString": "c:/test.txt","DBType": "","ProviderName": ""},"MariaDB": {"ConnectionName": "MariaDB","ConnectionString": "server=IPADDRESS;user id=root; password=mysql!@#$; database=sqlite_metadata;Port=3307;CharSet=utf8;","DBType": "","IsDefault": true, "ProviderName": "MySqlConnector","ServerVersion": "10,5,4"},"MysqlDB": {"ConnectionName": "MysqlDB","ConnectionString": "server=IPADDRESS;user id=root; password=mysql!@#$; database=sqlite_metadata;Port=3306;CharSet=utf8","DBType": "",
"IsDefault": false,"ProviderName": "MySqlConnector"}}|connection strings to replace the connectionsmanager.config files from version 3.x|
|CryptographyConfig|JSON|{"AES": {"key": ""},"EncriptionEnabled": "true"}|"EncriptionEnabled" - Decides if the sqlite_metadata.dataconnectionsmanager will be encrypted. The Key is important for the encryption and the decryption of the table|
|EndpointsConfig|List of strings|{ "ActiveDirectory""http://activedirectoryspi/api","AuditService": "http://auditservice/api","Authentication": "http://authenticationservice/api","Autoloader": "http://autoloaderservice/api","Cacheservice": "http://cacheservice/api","DataModelSearch": "http://datamodelsearchservice/api","Documentservice": "http://documentservice/api","EntityService": "http://entities-service:8080/EntitiesServices","Exportservice": "http://exportservice/api","FileServer": "http://IPADDRESS:5380/api","FreeTextService": "http://federated-search-service:8080/FreeTextService","Gatewayadminservice":"http://IPADDRESS:1025","Gatewayservice": "http://IPADDRESS:5070","GetLanguagesAzure":"https://api.cognitive.microsofttranslator.com","GetLanguagesSpi": "http://translationspi/api/Translation/GetLanguages","IndexingService": "http://indexing-service:8080/IndexingService","Linkanalysis":"http://linkanalysisservice/api","LoaderService": "http://loader-service:8080/LoaderService","MediaAnalyzer": "http://media-analyzing-service:8080/MediaAnalyzingService","MetaData": "http://metadataservice/api","PluginGateway":"http://IPADDRESS:5070/api","ReportGeneratorService": "http://report-generator-service:8080/ReportsGenerationService","SavedCriteria":"http://savedcriteriaservice/api","Schedulecriteria":http://schedulecriteriaservice/api","Schedulerservice":"http://schedulerservice/api","SensorsService":"http://sensorsservice/api","Speechtotextservice":"speechtotextservice/api","Speechtotextspi":"speechtotextspi/api","Taskservice": "taskservice/api", "TextAnalyticsService": "http://text-analytics-service:8080/TextAnalyticsService/textanalytics", "TranslateService": "http://translationservice/api", "TranslateSpi": "http://translationspi/api","TranslationAutoDetectAzure":"https://api.cognitive.microsofttranslator.com","TranslationAzure":"https://api.cognitive.microsofttranslator.com","UseHealthCheck":"true","UserManagement":"http://usermanagementservice/api","VmsService": "http://vmsservice/api"}|endpoints for services|
|ExternalUserManagement  |JSON  |"{""IsADEnabled"": true}"  |Will figure to know if AD is enabled  |
|FileServerConfig  |List of strings  |"{""FileServerDataCenterUrl"": ""http://IPADDRESS:8080"",  ""FileServerFilerUrl"": ""http://IPADDRESS:8888"",
  ""FileServerUrl"": ""http://IPADDRESS:9333"",  ""MaxUploadSizeBytes"": ""209715200""}"  |File server configuration  |
|FileTempExportPath  |string  |"{""path"": ""\\\\usr\\\\share\\\\Export""}"  |  |
|FileWatcherPath  |JSON  |"{""Extensions"": [""*.mp4"",""*.txt""],""path"":""/usr/share/vms""}"  |The path is where the camera recording you requested from VMS  |
|JWT  |JSON  |"{""Issuer"": ""TaAuthAPI"",""Key"": ""MySuperDuperSecretKey"",""TokenLifeTimeInSeconds"": 60000}"  |The Issuer and Key parameters are important to distinguish between 2 different environments  |
|JdbcConnectionStrings/DefaultConnection  |JSON  |"{""ConnectionString"":""jdbc:mariadb://IPADDRESS:3307/sqlite_metadata?serverTimezone=UTC"",  ""Password"": """",  ""Username"": ""root""}"  |JDBC connection string to sqlite_metadata  |
|JdbcConnectionStrings/OrientConnection  |JSON  |"{""ConnectionString"":""remote:IPADDRESS/TA9"",""Password"": """",""Username"":""root""}"  |JDBC connection string to OrientDB  |
|JdbcConnectionStrings/Rabbit  |JSON  |"{""ConnectionString"":""http://IPADDRESS:15672/api/exchanges/%2f/amq.default/publish"",  ""Password"": ""rabbit"",  ""Username"": ""rabbit""}"  |JDBC connection string to RabbitMQ  |
|JdbcConnectionStrings/ShortestPath  |  |  |  |
|LicenseKeysConfig  |List of strings  |"{""DocuViewareKey"": """",""SyncFusion"": """"}"  |License keys for DocuVieware and SyncFusion  |
|LinkAnalysisConfig  |List of strings  |"{""DefultQueryLimit"": ""50"",""Path"": ""path/linkanalysis/graph""}"  |The path where when a user is saving a graph  |
|ReportsGenerator  |List of strings  |"{ ""WindwardProperties"": ""WindwardReports.properties"",  ""WindwardWORKDIR"": ""/opt/app/data""}"  |Reports Generator config  |
|RpcConfig  |JSON  |"{""RabbitMq"": {""HostAddress"": ""IPADDRESS"",""Password"": ""rabbit"", ""Username"": ""rabbit"",  ""VirtualHost"": ""/""},""UseHealthCheck"": ""false""}"  |RabbitMQ configuration  |
|ServiceAdmin  |List of strings  |"{""Password"": """", ""UserName"":""ServiceAdmin""}"  |Service Admin configuration, if AD enabled still stays "ServiceAdmin" no need to append the domain  |
|Services  |List of strings  |  |Paths where the Text Analytics files exist  |
|ShortestPath  |  |  |  |
|SystemConfiguration  |JSON  |"{""OracleDefaultTablespace"": """",""PageSize"": 10000,""SolrFacetFieldQueryLimit"": 50,""SolrFacetMinParameterCount"": 1}"  |General system configurations  |
|TranslationApiConfigSettings  |List of strings  |"{""ContentType"": ""application/json"",  ""SubscribeKeyString"": ""Ocp-Apim-Subscription-Key"", ""TranslationHost"": ""api.cognitive.microsofttranslator.com"",  ""TranslationKey"": """"}"  |Translation congnitive service configuration  |
|TranslationServiceSettings  |List of strings  |"{""ContentType"": ""application/json"",  ""NumberOfCharsAllowedToTranslate"": ""10000"", ""SensorId"": ""15"",  ""TranslateFeatureName"": ""LiveTranslate""}"  |Translation service configuration  |
|UserLoginOptions  |string  |"{ ""IsSingleLogin"": ""false""}"  |If value is true only 1 session of the same user can be active  |
|VmsConfig  |string  |"{  ""ThirdPartyServiceUrl"": ""http://IPADDRESS:3004/vms/""}"  |VMS configuration  |
|VmsTokenConfig  |string  |"{""token"": ""Bearer TOKEN""}"  |VMS Token  |
|WatcherThreadPoolConfig  |string  |"{ ""workersNumber"": ""3""}"  |Config for how many threads of VMS can run at once  |


