[[_TOC_]]

# Loading Dates

## Solr based DM

Date format should be: YYYY-MM-DDThh:mm:ssZ or with Time Zone YYYY-MM-DDThh:mm:ss+HHMM (e.g. 2019-12-31T18:00:00+0200)

## MySQL based DM

Date format should be: YYYY-MM-DD hh:mm:ss 

## SAP IQ based DM

Date format should be: MM/DD/YYYY, for example: 10/17/1976

## OrientDB entities/relations format

UTC Date format should be: YYYY-MM-DDThh:mm:ss.SSSZ, for example: 2028-01-14T13:00:00.000Z
Another supported UTC format is without Z: YYYY-MM-DDThh:mm:ss.SSS, for example: 2028-01-14T13:00:00.000

In case time with time zone need to be used: YYYY-MM-DDThh:mm:ss.SSS+HH:MM, for example: 2028-01-14T13:00:00.000+02:00
