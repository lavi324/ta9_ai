[[_TOC_]]

## Intro
A tool for clearing & resetting the state of the AnyVision machine & TA9 integration data.
### Located at
https://dev.azure.com/ta-9/Argus/_git/Utils?path=%2FTools%2FResetAV

## What it does
1. Clear all **suspects** from AnyVision
1. Clear all **suspects groups** from AnyVision
1. Clear all **camera groups** from AnyVision
1. Clear all face-recognition **mappings** from IntSight MySQL
1. Clear all face-recognition **indexing-audits** from IntSight MySQL

## What it does NOT
1. Clear face-detection table
1. clear detection-rules table

Those 2 tables have to be **cleared manually** (if desired)

## Usage
`dotnet .\ResetAV.dll -mysqlurl localhost -mysqluser root -mysqlpass root -appurl 10.100.102.5:3000`

