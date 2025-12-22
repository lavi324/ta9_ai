[[_TOC_]]


# Intro
On version 2.14 we've added the feature of projecting not only lat/lon column-couples on map.
This feature includes only the presentation of such data (rather than querying/filtering on them).

# Data Types
1. WKT - Well Known Type string represnetation of geometries see https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry for more 
1. GeoJSON - json represnetation of geo features/geometries - see https://geojson.io/ for demonstration

# Usage on IntSight
## Definition (Admin)
Any WKT/GeoJSON field should be marked with Role = MainPoint/MainPolygon/MainLine

## Web Analyst
1. When showing a data model result on a map skin
In this case, any defined column that contains valid WKT/GeoJSON values is also shown on map as part of the data-model projected layer. Items should be drawn on the same color as other items of the same layer.
1. Wen using data-model as a layer on map
In this case, just like bullet \#1 - any additional values from defined columns, that contain valid WKT/GeoJSON values should be presented on map
2.1 **NOTE** - keep in mind that when using data-model-as-layer, we're filtering the layer on each map movement and show relevant items returned by filter. Since filtering is supported only on specific cases (see below) - this should be used with this note in mind


# Filtering
Currently, **no geo filtering is supported natively** by our platform, except the following implementations:
1. `lat/lon` bounding box
1. _Web Resource_ data-model (see https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/424/Data-Model-from-URL-Resource) that supports that kind of filtering (_EGIS_ for example)
1. Custom implementation via extension plugin
1. _Solr_ based data model that has a spatial field (native). This field has to be marked as follows:
4.1 `DataType = Point`
4.2 `Role = MainPoint`
In this configuration both quick-filtering & quiery-building are enabled for that field.

# Tech Notes
1. Data Model as Layer
1.1 Currently, when clustering (data model as layer), other geometries not taking part on the cluster, but returned one-by-one limitted by page-size
1.2 Cluster result's 'Name' prop returns geo type based on role (MainPoint/MainPolygon/MainLine) or empty when cluster
