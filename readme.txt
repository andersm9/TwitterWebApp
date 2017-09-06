This project is split into 2 parts
1)  Twitter monitor Service:
    provides a means to
    *monitor twitter for search terms
    *geocode the tweet
    *identify tweets within a set of predefined coordinates
    *send the tweets for sentiment analysis
    *save the tweets and metadata to a MySQL DB
    
2)  Results Display Service:
    The Flask framework
    *carries out a search of the MySQL db for the top 10 tweets by sentiment magnitude
    *passes the results to be tabulated within a web browser
    

This was developed using:

    Debian Jessie
    PyMySQL
    Python 3.4.2
    Flask 0.12.2
    MySQL Ver 14.14 Distrib 5.5.55
        the DB is set up as follows:
        DB name:    WebbApp
        Table name: Gitter
        Fields:
             Field     | Type         | Null | Key | Default | Extra |
            +-----------+--------------+------+-----+---------+-------+
            | TWEET     | varchar(128) | YES  |     | NULL    |       |
            | POLARITY  | int(11)      | YES  |     | NULL    |       |
            | MAGNITUDE | float        | YES  |     | NULL    |       |
            | LATITUDE  | float        | YES  |     | NULL    |       |
            | LONGITUDE | float        | YES  |     | NULL    |       |
            | NAME      | varchar(128) | YES  |     | NULL    |       |
            +-----------+--------------+------+-----+---------+-------+

    
You'll need Twitter and Google accounts with the relevant credentials to access the Twitter Streaming API and Google Sentiment Analysis and Geocoding APIs. All are free within certain limitations.
Git commands:

Source:

git add .
git add -m "comments"
git push origin master

AWS:

sudo su
cd to TwitterWebApp
git pull origin master

Screen commands:

screen -d -m <command>
screen -ls //see what processes are running
screen -X -S <ID> quit //kill process

DB

mysql -u root -p  /login
use WebAll
select * from Gitter