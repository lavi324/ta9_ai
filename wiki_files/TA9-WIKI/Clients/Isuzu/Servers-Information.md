
|  | Server Name | Operating System | Host Name | IP Address |port | Purpose | version | Installation path | Data Path |
|--|--|--|--|--|--|--|--|--|--| 
| 1. | intc2 | Windows Server 2016 | DIWINSRV02 | 10.100.102.90 | 443 | Indexing + Loader + TA9 System | 3.2 | Application | Application |
| 2. | Java + WildFly | Ubuntu 1804 | DIJAVSRV01 | 10.100.102.91 | 9900 |  Deploy java| 10.0.0 | /opt/application |  /opt/data |
| 3. | MySQL | Ubuntu 1804 | DISQLSRV01 | 10.100.102.92 | 3306 | System Configuration | 5.6 | /opt/application | /opt/data |
| 4. | Solr | Ubuntu 1804 | DISOLRSRV01 | 10.100.102.93 | 9500 | Document DB & Indexing | 6.1.0 | /opt/application | /opt/data |
| 5. | OrienDB | Ubuntu 1804 | DIORISRV01 | 10.100.102.94 | 2480 | Entities and Link Analysis  | 2.2.30 | /opt/application | /opt/data |
| 6. | SAP IQ | Centos 7  | DISYBSRV01 | 10.100.102.95 | 2638 | DB for Big Data Analytics | 16.0 | /opt/application | /opt/data |
| 7. | Syslog Server | Ubuntu 1804  | DILOGSRV01 | 10.100.102.97 | 9000 | Central Forensics Logs | 2.4.6-1 | /var/opt/graylog/data | /var/opt/graylog/data |
| 8. | Tile Server | Ubuntu 1804 | DITILSRV01(Non-Primary) | 10.100.102.98 | /hot/{z}/{x}/{y}.png | Maps Engine & DB | Latest | / | / |
| 9. | Tile Server | Ubuntu 2004 | DITILSRV02(Primary) | 10.100.102.101 | /hot/{z}/{x}/{y}.png | Maps Engine & DB | Latest | / | / |
| 10. | Nominatim | Ubuntu 1804 | DINOMSRV01 | 10.100.102.99 | /nominatim/ | Reverse Geocoding & DB | Latest  | / | / |
| 11. | PostgreSQL | Centos 7 | DIMERCUR01(Irrelevant) | 10.100.102.100 | 5432 | Mercure Data | 10.0 | / | / |
| 12. | PrizmDoc | Centos 7 | DIDOCSRV01 | 10.100.102.100 | 3000 | Document Viewer | 13.7| / | / |
| 13. | BriefCam | Windows Server 2016 | DIBFCSRV01 | 10.100.112.50 | NA | Video Synopsis | 5.6 | App | Data |
| 14. | AnyVision | Ubuntu 1804 | DIANVSRV03 | 10.100.112.11 | 3000 | Face Recognition | 1_20 | / | /storage |





