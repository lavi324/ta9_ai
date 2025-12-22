[[_TOC_]]

**THE NTP SERVER IS: DC1 - CADDCSRV01 - 10.100.118.10**

# Launch Powershell as Administrator and enable NTP server using the command:


```Set-ItemProperty -Path “HKLM:\SYSTEM\CurrentControlSet\Services\w32time\TimeProviders\NtpServer” -Name “Enabled” -Value 1```


## Configure Announce Flags value as shown

```Set-ItemProperty -Path “HKLM:\SYSTEM\CurrentControlSet\services\W32Time\Config” -Name “AnnounceFlags” -Value 5```

## Restart the NTP server using the command:

```Restart-Service w32Time```

# Add this configuration to all windows clients : 

```
netsh advfirewall firewall add rule name="NTP 123" dir=in action=allow protocol=TCP localport=123
netsh advfirewall firewall add rule name="NTP 123" dir=out action=allow protocol=TCP localport=123
```

# On Linux (centos) Machines

```vi /etc/ntp.conf```

```server 10.100.118.10 iburst```

```systemctl start ntpd.service```


# On Linux (Ubuntu 1804) Machines:

## install the service 
```sudo apt-get install ntpdate```

## Update host file
```sudo nano /etc/hosts```

## add this in the top of the configuration
```10.100.118.10   CADCSRV01.ecis.local```

## Open Port

```sudo ufw allow from any to any port 123 proto udp```

## Check configuration
```sudo ntpdate CADCSRV01```

![image.png](/.attachments/image-4e15dc73-abaf-4a75-890c-c174064a67b2.png)



# Set Time zone (Ubuntu + Centos)
``` sudo timedatectl set-timezone Asia/Jerusalem``` 

```sudo ntpdate CADCSRV01```

check the time : 

```timedatectl```








