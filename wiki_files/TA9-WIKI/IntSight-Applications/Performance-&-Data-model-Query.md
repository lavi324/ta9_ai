In case we have questions coming from clients/integrators on performance, here's a response that may help:

The data model is designed to support search across different types of technologies, 
as every technology supports searching in different ways.

While searching can be supported on different scales (small or huge) at the database engine, the data model was planned to use a certain page size in order to support the display of data in a web browser (performance is also related to the amount of memory that the client browser & PC have available).

Projects can contain hundreds of millions of records/entities, that eventually need to be displayed and investigated within the ability of the client.  
 
In Addition, from our experience even if we support 1M records it does not mean that you don’t miss those records which can be the most relevant, So in some cases where the result has the potential to return many records,  its good practice not to return the raw data but to build an aggregate query that reflects the summary of many records.

In case you want to return the raw data, the data model supports advanced build criteria to support the user to have more accurate filters in case he rich the page size.
The platform can support navigation between different pages if needed.