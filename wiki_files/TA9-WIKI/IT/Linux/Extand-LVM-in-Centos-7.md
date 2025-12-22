[[_TOC_]]

# List Disk
`df -kh`

# Show Volume extands
`lvs`

# List Disks

`fdisk -l`

# volume group display 
`vgdisplay`

# list the size of the logical volumes
`lvdisplay`

# list the size of the physical volume
`pvdisplay`

Extend the partition
`fdisk /dev/sda`

`p`

`n`

`p`

`t`

`p`

`w`


# Apply trhe settings
`partprobe`

Create the partition to extandable
`pvcreate /dev/sd`

# List partitins
`ls -l /dev/sd*`

# Create the extandable volume
`pvcreate /dev/sda3`

# list group of the volume
`vgdisplay`

# Extand the requiered volume 
`vgextend centos/root /dev/sdb`

# Pick how much to extand
`lvextend /dev/centos_centos7/root -L +XXXG`

# Resize the volume
`resize2fs /dev/centos/root`

# Mount it
`mount`

# Apply the settings 
`xfs_growfs /`

# observe the changes
`df -kh`


lvextend -r -l +100%FREE /dev/mapper/centos-root




