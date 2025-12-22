[[_TOC_]]

# 1. Install Nginx


```
sudo apt-get update
sudo apt-get install nginx
```

# 2. Disable the Default Virtual Host

`sudo unlink /etc/nginx/sites-enabled/default`

# 3. Create the Nginx Reverse Proxy
```
cd /etc/nginx/sites-available/
sudo vi reverse-proxy.conf
```


**Paste this**
```
server {
    listen 10.100.120.91:8040;
    location /{
        proxy_pass https://nginx-localnode.tls.ai/;
    }
}
```
Save and quit.


# 3.1 activate the directives by linking to `/sites-enabled/ `
`sudo ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf`


# 4. Test Nginx and the Nginx Reverse Proxy
```
sudo service nginx configtest
sudo service nginx restart
```

# 5. Open Firewall ports

`sudo ufw allow from any to any port 8040 proto tcp`

# 6. Test configuration

http://10.100.120.91:8040/pipe_store/tracks/5ece5d5e093961002736a3f9/27-05-2020/5LKNCDHH/LargeDetection-00000.jpg












