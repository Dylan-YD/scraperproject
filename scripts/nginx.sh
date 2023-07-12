
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/scraper/nginx/nginx.conf /etc/nginx/sites-available/scraper
sudo ln -s /etc/nginx/sites-available/scraper /etc/nginx/sites-enabled/
#sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled
#sudo nginx -t

sudo gpasswd -a www-data ubuntu
sudo chown -R www-data:www-data /home/ubuntu/scraper

sudo systemctl restart nginx

