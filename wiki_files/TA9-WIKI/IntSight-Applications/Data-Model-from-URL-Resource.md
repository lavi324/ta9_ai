[[_TOC_]]
Video tutorial 
https://web.microsoftstream.com/video/a989076c-0d9a-4a8d-8194-5766834ccc96

# Intro
On version 2.13 we're adding the first implementation of the feature "_Data Model by URL_".
The purpose of this feature is to enable a full _Data Model_ usage based on a web resource. For example, there's a web resource (e.g _web-service_) that returns all credit card transactions and allows to filter them by country, card type, etc. We'd want to create a data-model on top of that resource so that the user can use the data returned by that service regularly across the system (e.g defintion of the _Data Model_ and then querying, filtering, indexing, etc.)

# Usage
## Definition
On _IntSight Admin Console_, a new provider is added - **Web Resource**.
To define a new _web-resource Data Model_, click a _Web Resource_ provider, then a popup to input 2 fields will appear:
1. **URL** - the URL of the resource. This URL should return values (ie - **don't** input here the format)
1. **JSON Path** - path of the results within the JSON response of the web resource. This path must point to a **valid JSON array of objects**

![image.png](/.attachments/image-9f4fd7e7-c8dc-4c14-83fb-9f32bd161e5a.png)

Once we've input valid values and click OK, we navigate to the familiar data-model configuration window. Fields are automatically created from the sample URL & JSON path provided. 
Here, we can configure our _web resource data model_ with the following options:
1. **URL Format** - here we can/should add some parameters to our URL (otherwise all that data model's queries return same results). 
The URL support the following format options:
   1. `{FieldName}` - any field of the data model can be used in the URL wrapped in curly brackets. If this field is queryable (i.e QueryBuilder/FreeText/QuickBuilder etc.), when using it as a filter - that filter's value is replaced with the field value in URL when querying the data model.

**NOTE:** fields can be added and formatted into the URL in order to support various filters
![image.png](/.attachments/image-e97e7d5c-216f-4ea4-878d-8d90d712e4ad.png)

   1. {{page}} - this reserved word is replaced with current page of the data model query
   1. `{{pageSize}}` - this reserved word is replaced with defined page size of the  data model
   1. **Geographic Fields** - geographic fields can be added regularly as other fields to the URL. Additionally, they support also a _BBox_ formatting:
`{GeoFieldName.BBox[MinX]}` (square brackets support `MinX / MinY / MaxX / MaxY`)
    4.1 When filtering on specific fields - they're added by their name
    4.2 When filtering on main location - all `MainLongitude/MainLatitude/MainPolygon` fields can be used in the format

1. **Fields** - firstly, all field are auto generated from the first object of the array fetched from the URL given when creating the data model. Then, fields can be added and removed regularly and they will behave as any other data model fields.
    1. **FieldName** - field's `FieldName` should point to a JSON property path within the object, ie - in this way the JSON object can be "_flattened_" to our needs. So, for example, we can add a field `'address.geo.latitude'` and it will contain the nested value of a JSON object within the results array

## Analyst
Use this data model within the system as any other data model.
Once defined well it supports:
- Querying
- Filtering
- Free Text Search
- Indexing
- Map Skin
- Link Analysis Skin
- Data Model as Layer

# Constraints/Known Issues/Next Steps
1. Only GET requests are supported (#39317)
1. Only JSON responses are supported (#39320)
1. No additional headers/authorization can be added (#39319)
1. GetSampleData does not fill in nested fields (e.g address.geo.lat) (#39318)
1. URL format/JSON path cannot be edited AFTER data model is created
1. No loading is relevant to this data model type
1. When using multiple values for a filter - they're concatenated as CSV on formatting
1. When doing BBox of a polygon - if multiple polygons are sent - only the first one is taken


# Tech Notes
1. Web resource parameters are saved as:
   1. TableName stores the URL format (with parameters as defined on the data-model configuration screen)
   1. SchemaName stores JSON Path as defined on the data-model configuration screen
   1. Connection only stores values for initial data model definition (ie - when initialy entered values to the popup). Not relevant for usage.

# Relevant Ticket:
https://dev.azure.com/ta-9/Argus/_workitems/edit/39316