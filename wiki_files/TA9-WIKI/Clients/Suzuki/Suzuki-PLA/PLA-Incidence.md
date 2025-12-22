       
**PLA Incidence**
**The PLA (Post Loading Action)** is responsible for handling incidents received from upstream data sources, analysing them, and triggering the appropriate entity creation workflows. It acts as a central service for processing structured event data before pushing it to downstream systems such as entity creation and detection modules.
Previously, PLA processed incidents synchronously without any queue. While the original design was effective for its scope, it did not include mechanisms for tracking or error handling. Once an incident was inserted into PLA, there was no way to monitor whether the process succeeded or failed. Retry logic, error monitoring, and execution control were not part of the initial architecture, which followed a “fire and forget” pattern similar to the IOC logic.
The new design introduces a queue into PLA: instead of immediately processing the incident, PLA places the data into a queue. A separate process then consumes the message and performs the entity creation logic. This allows the system to monitor the status of the operation, retry failed events, and — when needed — perform manual insertion into the system.
🟩 Queue-Based Insertion Logic  
PLA now inserts each incoming incident into a queue instead of processing it immediately. This introduces an asynchronous workflow and decouples data ingestion from entity creation. It also creates an opportunity to manage the process in a more controlled and observable manner.
🟩 Consumer Execution Model  
A dedicated internal component (the Consumer) continuously listens to the queue. Once a message is received, the Consumer executes the entity creation logic based on predefined configurations, including:  
- Entity type  
- Relationship mappings  
- Data structure  
- Additional metadata as needed  
  
These configurations can also support specialized flows such as fraud detection use cases — including the Anti-Scam solution described below.
🟩 Entity Creation with Specialized Use Cases (e.g., Anti-Scam)  
As part of the entity creation process, the system supports enhanced data models such as the Anti-Scam solution. This includes logic to detect and handle different types of entity alerts:  
- New entities not previously seen in any incident  
- Existing entities found across multiple incidents  
- Newly discovered entities specific to the current incident  
  
  

These detections are configured via dedicated alert types and are stored in a separate data model (Anti-Scam Notifications). Entity matching is based on identifiers such as phone numbers, email addresses, bank accounts, and others. This logic extends the flexibility of the PLA entity creation to support real-world fraud detection and analytical scenarios, without changing the core flow.
🟩 Entity Extraction Using Text Analytics Service  
In PLA's architecture, certain fields in Solr (such as Regex-based identifiers) are not automatically populated. To enhance entity extraction from the incident's description field, the system utilizes a service called Text Analytics. This service is responsible for identifying and extracting entities from free-text descriptions.  
  
Entity extraction is performed using either:  
- NER (Named Entity Recognition) — for dynamic, context-based entity identification  
- REGEX (Regular Expression)— A rule-based method used to extract structured data.  
  
The REGEX patterns used in the system are defined based on identifiers (e.g., phone numbers, email addresses, account numbers), and configured accordingly in the backend to match and tag relevant data fields. 
Most of the entity patterns used in this project are based on highly specific Regex expressions, such as national ID numbers (NRIC), license plate numbers, and other domain-specific identifiers. In addition to their use in Text Analytics, these patterns also play a key role in the bulk data insertion process.

🟩 Failure Handling and Retry Mechanism  
If the entity creation process fails, the message can be re-queued automatically or handled manually. This enhances reliability and allows for post-failure recovery — a feature that did not exist in the previous model. This also enables tracking and analyzing failure causes in a structured way.
🟩 Token and Gateway Propagation Challenge
Since the insertion is now outside the PLA scope, a challenge arose regarding how the new service receives the Token and Gateway URL. 
Initially, the intended solution was to pass the token with the incident data.
However, for security reasons, the token is no longer included in the message.
Instead, the service now uses a dedicated username and password, defined in the configuration file.
The Gateway URL is also included as part of this configuration.

* * *

Most of the entities are based on specific regex (unique to this project such as NRIC, license plate) , on another hand this part of insert bulk data process.

![Picture1.png](/.attachments/Picture1-39483336-b386-4fff-a3ce-73d51d9e2cd1.png)







      
This diagram (after the explanation) illustrates the logical flow of data within the PLA process. It highlights the core business logic — from data ingestion through queueing, entity creation, and alert detection — without reflecting the underlying infrastructure or service-level components such as databases, configuration files, or API gateway logic. It is intended to provide a conceptual understanding of how data and logic are processed inside PLA.
![{F880606E-C358-458A-8696-A2865953680C}.png](/.attachments/{F880606E-C358-458A-8696-A2865953680C}-7f9ddb93-a88b-48ec-82d8-45693996c541.png)

