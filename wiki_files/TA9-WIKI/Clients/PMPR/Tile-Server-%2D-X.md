[[_TOC_]]

# Machine to use:

Custom -TileServer

Host: 10.100.102.8


# Get the maps 

## Europe

```
wget https://download.geofabrik.de/europe-latest.osm.pbf
```

## Africa
```
wget https://download.geofabrik.de/africa-latest.osm.pbf
```

## Asia
```
wget https://download.geofabrik.de/asia-latest.osm.pbf
```

# Merge maps:
```
sudo apt install osmium-tool
osmium merge europe-latest.osm.pbf africa-latest.osm.pbf asia-latest.osm.pbf -o X-maps.osm.pbf
```

# Load maps

```
osm2pgsql -d gis --create --slim  -G --hstore --tag-transform-script ~/src/openstreetmap-carto/openstreetmap-carto.lua -C 31000 --number-processes 8 -S ~/src/openstreetmap-carto/openstreetmap-carto.style ~/data/X-maps.osm.pbf
```

# Create the Shapefile 

cd ~/src/openstreetmap-carto/
scripts/get-external-data.py

