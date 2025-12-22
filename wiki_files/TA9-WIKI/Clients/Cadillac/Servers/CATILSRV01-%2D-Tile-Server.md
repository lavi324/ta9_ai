[[_TOC_]]

# Prerequisite

## Operating system
Ubuntu 1804 

## Environment
Dedicated to host

## OVA File location
\\10.100.102.13\share\ Clients\Cadilac\TA9_TileServer\Maps

## VMWare configuration

Use Thin disk.

# Install the server

Followed by this guide: 

[https://switch2osm.org/serving-tiles/manually-building-a-tile-server-18-04-lts/]()


## add custom user

Become Root:
`su -i`

Add user home directory:
`useradd -m -d /home/ta9cad/ -s /bin/bash -G sudo ta9cad`

Add user to administrators group:
`usermod -aG sudo`


#Required Map

Cadilac.osm.pbf

\\10.100.102.13\share\Clients\Cadilac\WE-Cadilac-TileServer\Maps


# Create Database for Cadilac map
`sudo -u postgres -i`
`createuser root` 


##Alter Tables gis
```
psql
\c gis
CREATE EXTENSION postgis;
CREATE EXTENSION hstore;
ALTER TABLE geometry_columns OWNER TO root;
ALTER TABLE spatial_ref_sys OWNER TO root;
\q
```

# Create user for rendering
useradd -m -d /home/ta9cad/ -s /bin/bash -G sudo ta9cad


# Load maps to the server
## Switch to ta9cad
`su - ta9cad` 

##Cadilac
```
osm2pgsql -d gis --create --slim  -G --hstore --tag-transform-script ~/src/openstreetmap-carto/openstreetmap-carto.lua -C 2500 --number-processes 1 -S ~/src/openstreetmap-carto/openstreetmap-carto.style ~/data/Cadilac.osm.pbf
```

**If Success**
![image.png](/.attachments/image-1f8c8af2-e758-495c-8900-4031db480f82.png)



# Setting up your webserver

## Configure renderd

`sudo nano /usr/local/etc/renderd.conf`


```
num_threads=100
XML=/home/ta9cad/src/openstreetmap-carto/mapnik.xml
URI=/hot/
```

## Configuring Apache

`sudo mkdir /var/lib/mod_tile`

`sudo chown ta9cad /var/lib/mod_tile`

`sudo mkdir /var/run/renderd`

`sudo chown ta9cad /var/run/renderd`

## run this twice
```
sudo service apache2 reload
sudo service apache2 reload
```


# Running renderd in the background

Next we’ll set up “renderd” to run in the background. First, edit the “~/src/mod_tile/debian/renderd.init” file so that “RUNASUSER” is set to the non-root account that you have used before, such as “ta9cad”, then copy it to the system directory:

`nano ~/src/mod_tile/debian/renderd.init`


```
sudo cp ~/src/mod_tile/debian/renderd.init /etc/init.d/renderd
sudo chmod u+x /etc/init.d/renderd
sudo cp ~/src/mod_tile/debian/renderd.service /lib/systemd/system/
```

`sudo /etc/init.d/renderd start`

`sudo systemctl enable renderd`
`systemctl restart renderd`
`systemctl stop renderd`
`systemctl start renderd`
