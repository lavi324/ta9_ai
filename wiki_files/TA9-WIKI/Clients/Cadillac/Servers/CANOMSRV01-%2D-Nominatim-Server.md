[[_TOC_]]

# Prerequisite

## Operating system

| Required OS |Ubuntu 1804  |
|--|--|
| IP Address | 10.100.120.88 |
| Port	 |NA|
|Hostname	|  CALOGRV01|
| User	 | NA |

The image stored on the ESXI vSphare server.

All you need is the map, will give separately .
To load map: 

```
su – nominatim
cd build/
./utils/setup.php --drop
./utils/setup.php --osm-file NewCadilac.osm.pbf --all 2>&1 | tee setup.log
```

This process will take some time.
















