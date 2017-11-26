Tested on Ubuntu 16.04

1. Install the following packages

    `sudo apt install git nginx python-pip uwsgi uwsgi-plugin-python mysql-server python-django python-django-common`

    
1.5 Setup mysql root account
    (If mysql didn't automatically prompt you for a password for the root account run the following command:)

    `mysql_secure_installation`
    
    Login to mysql
    `mysql -u root -p`
    
    Run the following line
    `uninstall plugin validate_password;`
    
    Disconnect from the mysql DB
    
1.7 Kill the current Nginx process
    (nginx likes running from install)
    
    `sudo nginx -s stop`

2. Using pip, install the following modules

    `sudo pip install PyMySql lxml`

3. Create the nginx user

    `sudo adduser nginx`
    
    `sudo usermod -aG sudo nginx`

4. Sign in as nginx and prep directories

    `su nginx`

5. Make the following directories

    `mkdir /home/nginx/www`

6. In the directory you just made

    `git clone https://github.com/CSCC01F17/L01_03`

7. Copy the code over

    ```cp L01_03/project/Back-End/Cgi/ . -r
    cp L01_03/project/Back-End/init/ . -r
    mkdir html/
    cp L01_03/project/Front-End/* html/
    cp L01_03/project/Front-End/Dev/* html/ -f```

8. Replace the prod config with the non-prod config

    `cp L01_03/project/Back-End/Dev/* . -r`

9. Copy the nginx conf file to /etc/nginx/nginx.conf

    `sudo cp init/nginx.conf /etc/nginx/nginx.conf`

    Nginx doesn't like the -c argument with ubunto 16 for some reason


10. Setup the mysql server

    `mysql -u root -p <L01_03/project/Back-End/setupSql.sql`

11. Start nginx

    `sudo nginx`

12. Start uwsgi

    `sudo uwsgi --ini init/uwsgi.ini`

Congratulations, the server is now running!

If you would like nginx and uwsgi to automatically restart, follow your distro's guide for systemd or its equivalent using the nginx.system, and uwsgi.system files in the init/ folder

