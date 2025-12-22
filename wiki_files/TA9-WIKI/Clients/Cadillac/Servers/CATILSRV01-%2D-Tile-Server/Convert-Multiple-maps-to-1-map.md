[[_TOC_]]

#Required Ubuntu Server

#Download the required maps
##Create a directory
`mkdir maps && cd maps/`


##Cyprus
wget https://download.geofabrik.de/europe/cyprus-latest.osm.pbf

##Greece

wget https://download.geofabrik.de/europe/greece-latest.osm.pbf

##Turkey

wget https://download.geofabrik.de/europe/turkey-latest.osm.pbf


`apt install osmium-tool`

# Convert  
so you can merge all of them in one file

osmium merge greece-latest.osm.pbf  cyprus-latest.osm.pbf -o greccecyprus.osm.pbf

osmium merge greccecyprus.osm.pbf  turkey-latest.osm.pbf -o All3maps.osm.pbf

## Apply on gis database

osm2pgsql -d gis --create --slim  -G --hstore --tag-transform-script ~/src/openstreetmap-carto/openstreetmap-carto.lua -C 2500 --number-processes 1 -S ~/src/openstreetmap-carto/openstreetmap-carto.style ~/data/backup/All3maps.osm.pbf