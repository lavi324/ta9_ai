- **What or how does TA9Insight detect or sniff out correlated incident?** Correlated incident based on predefined algorithm with business logic that considers time and location.
- **Does entity link analysis depend on all the data ingestion into SMP FOC?** Entities and relations created in the system in various ways. It can be based on manual creation or based on PLA that runs automatically and extract entities from each incident.
- **What is the current methodology or approach that will be using for FOC?** Does FOC need to ingest all the data in order to build the link analysis network?]
The methodology in FOC includes the various ways I have mentioned, both manual and automatically. The automatic way which based on PLA ingest all the incidents received in the system, using relevant information extracted from the incident itself to build the network.
- **How does the Enterprise search or federated search works?**  This is Google like search. Cross-system search for unstructured data, that allows to search across all the data that is indexed in the system. This feature keeps the users’ search-phrase history, Highlight the search term, apply facet filters, advanced search capacities, change sorting and more.
- **Does the search feature query past incidents?** The federated search able to query all the data that indexed to the system, including past incidents. The search feature in the SitPic in the upper toolbar allows to search past incident which can be filtered by range of dates as well.
- Does TA9Insight ingest all the incidents that was passed in via MQ? TA9Insight ingest all the incidents via the MQ. 
- **Can User upload SOP/Job aid on their own?**  Incidents Protocol is a feature that allows the user to manage a group of tasks that has to be done when incidents occur – known as the incident “Protocol”. The Protocol management tool (located on the admin tools) allows managing protocols, creating, editing, and assigning relevant incident types. Only Admin user can upload or edit protocols.
- **Can we limit to who can edit or delete the annotation and drawing done at the visual analysis?**  Any user with permission to incidents can edit or delete the visual analysis. The permission is controlled by permission to the incidents data model. 
- **Can explain where are visual analysis data being stored and how are they linked?**  The data stored in TA9 MariaDB, linked to the incident.
- Can explain where are visual analysis data being stored and how are they linked?  The data stored in TA9 MariaDB, linked to the incident.
- **How about multimedia attachment or office document?** Where are they being stored?]                              Multimedia stored in the Maria DB. Documents stored is the Solr DB.
- Does visual analysis supports concurrence editing? Once a user adding visual analysis to an incident and saves it, other users can see and edit the drawing.
- **Prior to user saving the visual analysis, does it means other users will not be able to see it?** Is there an auto-saved featured?]
While editing the visual analysis other users are not able to see it. Only once the visual analysis is save other users are able to see it. There is no auto-saved feature.
- **Does it keep indefinitely?** The visual analysis saved without defined time limitation.
- **In SMP FOC, can we configure the permission to group / role level who can download the attachment?**  Same as visual analysis – every user with permission to the incidents can download the attachments of the incident.





