[[_TOC_]]

sp_helptext UpdateSubscriberCDR

# Introduction
While loading data to the 'CDR' (or in its French name 'Fadet') Data Model, a stored procedure is triggered.
Some of the 'Fadet' fields are enriched by other data from the different data models, guided by pre-defined fields.
# The 'CDR' Fields Enrichment In Intc2
In the table below you can see:
- The enriched 'CDR' field.
- The enriching data model.
- The enriching fields.
- The fields that the 'CDR' is enriched from, the linking fields.

![image.png](/.attachments/image-61020233-2abb-442c-879e-966fcac98e84.png)

> **Note!** On Jul 23 we created a new Unified subscribers table and a new SP, in order to improve CDR loading performance & time. Details are found in this link: https://ta9comp.sharepoint.com/:t:/s/businessteam/ETiIpdWqdmFEoLrbcub2ECMBc_LDNXeiKov77iLWzuSJJQ?e=PoMSey 


Other Enrichments:
1. Geo Hash - Adding the Geo Hash Value from the BTS table, into the CDR table based on the Cell found (Cell must contain Geo Hash Values)

_For more information on Adding Geo Hash values:_
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/556/UPDATED-Adding-new-BTS-Data-(Cell-Towers)

2. Is Technical - Using a Predefined data model that contains technical numbers, we enrich the CDR information to mark Yes/No if the number in the CDR is technical or not.

_For more information on Technical numbers:_ 
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/715/Technical-Numbers-enrichment
