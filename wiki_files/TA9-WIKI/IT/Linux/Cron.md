

![image.png](/.attachments/image-fd88ce08-0d61-4c1d-9cb0-961f7f5af306.png)

[[_TOC_]]

# Introduction

The software utility cron is a time-based job scheduler in Unix-like computer operating systems

## Schedule task 

To delete files older then 30 days:

`find /path/to/files -mtime +30 -exec rm  {}\;`

The syntax to Cron: 

`* * 31 * * sudo find /opt/wildfly/log/* -type f -mtime +30 -exec rm -rf {} \; >/dev/null 2>&1`




