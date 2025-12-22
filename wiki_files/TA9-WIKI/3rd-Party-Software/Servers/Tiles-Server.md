[[_TOC_]]
#Introduction
IntSight supports and able to connect to any Tile server follow the following conventions:
* Tiles are 256x256 pixels
* At the outermost zoom level, 0, the entire world can be rendered in a single map tile.
* Each zoom level doubles in both dimensions, so a single tile is replaced by 4 tiles when zooming in. This means that about 22 zoom levels are sufficient for most practical purposes.

The de facto OpenStreetMap standard, known as Slippy Map Tile names or XYZ, follows these and adds more:
Images are served through a Web server, with a URL like http://.../Z/X/Y.png, where Z is the zoom level, and X and Y identify the tile.

In addition, IntSight supports Bing Maps & OpenStreetMap (OSM) in case of an internet connection.

OpenStreetMap (OSM) is a collaborative project to create a free editable map of the world. The geodata underlying the map is considered the primary output of the project. The creation and growth of OSM have been motivated by restrictions on the use or availability of map data across much of the world, and the advent of inexpensive portable satellite navigation devices.

#Installation
##Centos installation guide
https://switch2osm.org/serving-tiles/manually-building-a-tile-server-18-04-lts/
## Installation with docker


```
docker volume create openstreetmap-data

import
docker run -v /home/ta9/installs/israel-and-palestine-latest.osm.pbf:/data.osm.pbf -v openstreetmap-data:/var/lib/postgresql/10/main overv/openstreetmap-tile-server import

docker volume create openstreetmap-rendered-tiles
docker run --name OSMTiles -p 80:80 --restart=always -v openstreetmap-data:/var/lib/postgresql/10/main -v openstreetmap-rendered-tiles:/var/lib/mod_tile -d overv/openstreetmap-tile-server run
```

* You can download different maps to load from: http://download.geofabrik.de/
* Please note - to install a large map like the whole world you'll need:
  * 64 GB ram
  * 8 CPU Cores
  * 1.5 Tera SSD storage
    not using SSDs will make the whole process really long, approximately a week.   


#Troubleshooting 
## Enable cross-origin headers in apache2 (on Ubuntu):
1.	Enable to headers module:
  a.	cd /etc/apache2/mods-available
  b.	Create a file named ‘headers.load’
  c.	Write a single line in the file:
  i.	LoadModule headers_module /user/lib/apache2/modules/mod_headers.so
  d.	sudo a2enmod headers
  e.	Add the following lines in /etc/apache2/sites-enabled/000-default.conf (right before the closing tag </VirtualHost>)
    1.	Header always set Access-Control-Allow-Origin "*"
    1.	Header always set Access-Control-Allow-Methods "GET "
    1.	Header always set Access-Control-Allow-Headers "Content-Type"
2.	sudo service apache2 restart

## Can't view image tile from TA9 IntSight web client due to invalid certificate
In case the tiles server certificate is invalid or from an internal authority, chrome won't approve downloading the tiles for the user, in this case, please do the following: 
1. Try open the tiles server URL from Chrome browser
2. In case warning appears, click Advanced
3. Then click Proceed
4. In case the tiles server is now accessible refresh the IntSight client and the map tiles should appear.



# How To Move a PostgreSQL Data Directory

OS : Ubuntu 1804
Postgresql Version : 10

## 1. verify the current location
```
sudo -u postgres psql
SHOW data_directory;
q\
```
![image.png](/.attachments/image-b89e9c52-dcaa-41b3-babc-78c629d6862e.png)

### Stop Service
```
sudo systemctl stop postgresql
sudo systemctl status postgresql
```
![image.png](/.attachments/image-75b16f68-0729-4849-93a2-9107f37c6a9a.png)

### Sync all PostgreSQL File
```sudo rsync -av /var/lib/postgresql /mnt/NEWLOCATION```

### Create BackUp
```sudo mv /var/lib/postgresql/10/main /var/lib/postgresql/10/main.bak```


## 2. Pointing to the New Data Location

```sudo nano /etc/postgresql/10/main/postgresql.conf```

data_directory = '/mnt/volume_nyc1_01/NEWLOCATION/postgresql/10/main'


## 3. Restarting PostgreSQL
```sudo systemctl start postgresql```

### confirm that the PostgreSQL server started successfully
```sudo systemctl status postgresql```

### Check data location
```
sudo -u postgres psql
SHOW data_directory;
\q
```

If database is in the new location you can remove the backup

```sudo rm -Rf /var/lib/postgresql/10/main.bak```





