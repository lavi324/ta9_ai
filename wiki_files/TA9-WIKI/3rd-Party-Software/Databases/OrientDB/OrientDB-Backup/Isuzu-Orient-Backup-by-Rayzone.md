Since RZ is responsible of backups in our shared project, they have shared with us the script they use for 3.9.x versions:

In the old version of Orient it does not really support backup functionality, but it does support full data export.
What we do is as part of daily backup of virtual machine, before the backup we run a script that performs full export to the disk, and when the VM is backed up consistent copy is saved on that backup disk.
We also change the name of backup using date as part of it, so we can keep N backups back if needed, and we also additionally copy the orient config folder to keep config in addition of the data itself.
 
Adding Leonid Gvirtz here in CC in case I missed something in this explanation.
 
The full backup script is
 
*#!/bin/bash
 
ORIENTDB_HOME='/opt/application/orientdb-3.1.10'
ORIENTDB_USERNAME=root
ORIENTDB_PASSWORD='ENTER_PASSWORD_HERE'
EXPORT_DEST_DIR=/opt/archive
FILETIMESTAMP=$(date +"%Y%m%d%H%M%S")
 
rm -fr $EXPORT_DEST_DIR/export_TA9_full_*.gz
$ORIENTDB_HOME/bin/console.sh "connect remote:localhost/TA9 $ORIENTDB_USERNAME $ORIENTDB_PASSWORD;export database $EXPORT_DEST_DIR/export_TA9_full_$FILETIMESTAMP"
 
rm -fr $EXPORT_DEST_DIR/config
cp -R $ORIENTDB_HOME/config $EXPORT_DEST_DIR
 
 
you can check it on orient db production server located at /bu_scripts/backup_orientdb.sh

*need to remove the * since this wiki thinks it a syntax for a title.