# Map Services Offline Services Installation Guide

This guide is intended for users who want to set up an OpenStreetMap (OSM) tile server and Nominatim for offline use.

The installation process requires downloading the necessary map data and setting up the server to serve tiles and
geocoding requests without relying on external services.

Constructing the tile server and Nominatim for offline usage is a complex process that requires significant resources
and time.

## Required Resources

The CPU, memory and storage requirements for an OpenStreetMap (OSM) tile server vary significantly depending on several
factors, including:

- Geographic coverage: A server for a single city or country will require far less resources than one serving the entire
  planet.
- Traffic volume: The number of users and tile requests per second/month will heavily influence the necessary hardware.
- Geographic data: Image type, zoom levels and map styles influence storage and processing demands

### Common scenarios:

- Small Scale (City or Small Country, Low Traffic)
- Medium Scale (Large Country/Region, Moderate Traffic):
- Large Scale (Entire Planet, High Traffic):

| resource | small    | medium      | large       |
|----------|----------|-------------|-------------|
| CPU      | 4-8 core | 8-16 cores  | 16-24 cores |
| RAM      | 12 GB    | 24-64 GB    | 128-384 GB  |
| Storage  | 300 GB   | 500-1500 GB | 3-6 TB      |

## Prerequisites

- Linux server with Docker and Docker Swarm
- Root permissions
- Stable internet connection (for initial setup)

## Installation steps

### 1. Data Preparation

1. Download map data (.osm.pbf) from https://download.geofabrik.de/
2. Place downloaded file in `stacks/osm/data/`

> **OSM and Nominatim can be installed in parallel**

### 2. OSM Tiles Server Setup

1. Set the map data file and path for the tile server. update `stacks/osm/env.local.peroperties` (if the file not exists
   create from a template file)

   ```properties
   PBF_FILE=data/<you data file name .osm.pbf>
   ```

2. Create and set data paths with **root** permissions
   ```properties
   OSM_PATH_DB=/opt/data/osm/database
   ```

3. Run the setup script to initialize the tiles database
   > **⚠️ Important**: 
   > - This step requires a stable internet connection to download the necessary data files.
   > - The setup script may take a long time to complete, depending on the size of the downloaded data file and
   > - for long-lasting run use the '-b' option to run in the background.

   ```bash
   cd stacks/osm
   ./osm_tiles_setup.sh 
   ```
4. deploy the `osm` stack
   ```bash
   ./deploy.sh -f osm
   ```

### 3. Nominatim Server Setup

1. Set the map data file and path for the tile server. update `stacks/nominatim/env.local.peroperties` (if the file not
   exists create from a template file)
   ```properties
   PBF_FILE=data/<you data file name .osm.pbf>
   ```
2. Create and set data paths with **root** permissions
   ```properties
   NOMINATIM_PATH_DB=/opt/data/nominatim/db
   NOMINATIM_PATH_FLATNODE=/opt/data/nominatim/flatnode
   ```
3. Deploy the Nominatim stack
   > **Important**: On the first deployment, the Nominatim setup script will extract the necessary data files and
   > set up the database. It depends on the data file size and the server's resources; this step may take a long time to
   complete.

   ```bash
   ./deploy.sh -f nominatim
   ```

### 4. Update Service URLs
Update `sqlite_metadata.endpoints_manager` with:
- OSM: `http://<server address>:8080`
- Nominatim: `http://<server address>:8181`
