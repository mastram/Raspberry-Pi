Step by Step guide to install LAMP and post setup

#### First step is to install apache
`sudo apt-get install apache2 -y`

#### Next step is to install PHP
`sudo apt-get install php -y`

#### Next step is to install MySQL
`sudo apt-get install mysql-server php-mysql -y`

#### Next step is to install PhpMyAdmin
`sudo apt-get install phpmyadmin`

Then restart apache service
`sudo service apache2 restart`

#### Change root directory of Web