# Deleting entity and its relations
```
!!! Disclaimer !!!
- The following steps will erase data and schema from orient db which can't be restored.
- Partial execution will lead to inconsistency in the data
- Process may result corrupt database. ensure the database is fully backup before starting.
```
In case you need to drop entity class and its relations from OrientDB, first drop relations than drop the entity.

## Connect to OrientDB CLI
Run:
- `bash bin/console.sh`
- `CONNECT remote:localhost/TA9 root`
- type password


## Deleting Relations
Run the following commands for **every** relation that needs to be deleted.

- `DELETE EDGE RL<X>`
- `DROP CLASS RL<X>`

Make sure you change the relation name to its actual name, for example, RL3.

## Deleting Entities
Run the following commands for the entity that needs to be deleted. 

- `DELETE VERTEX EN<X>`
- `DROP CLASS EN<X>`

Make sure you change the entity name to its actual name, for example, EN3.