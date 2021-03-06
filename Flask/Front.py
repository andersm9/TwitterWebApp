#!/usr/bin/python3


from flask import Flask, render_template, request, json, Response
import pymysql.cursors
import logging
logging.basicConfig(filename='Front.log',level=logging.WARNING)

app = Flask(__name__)
#mysql = MySQL(app)
# MySQL configurations
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'Gitter'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app)
#db2 = MySQLdb.connect("localhost","root","root", "WebApp")
#cursor = db2.cursor()

#PyMYSQL db
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='WebApp',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor,
                             connect_timeout=288000)
@app.route("/")
def main():
    #set long timeouts on SQL
    with connection.cursor() as cursor:
        sql1 = "SET SESSION wait_timeout = 999999"
        cursor.execute(sql1)
        sql2 = "SET SESSION interactive_timeout = 999999"
        cursor.execute(sql2)
        cursor.close()       
    try:
        with connection.cursor() as cursor:
    # Read a single record
            sql = "SELECT TWEET, POLARITY, MAGNITUDE, LATITUDE, LONGITUDE, NAME FROM Gitter ORDER BY MAGNITUDE DESC LIMIT 30"
            cursor.execute(sql)
            result = cursor.fetchall()
            #sql3 = "SHOW VARIABLES LIKE 'interactive_timeout'"
            #cursor.execute(sql3)
            #result = cursor.fetchall()
            cursor.close()
            print (type(result))
            print (result)
        #print ("   ")
    
#MySQL    
    #get the top 10 rows (by "MAGNITUDE") in the DB
    #cursor.execute("SELECT TWEET, POLARITY, MAGNITUDE, LATITUDE, LONGITUDE, NAME FROM Gitter ORDER BY MAGNITUDE DESC LIMIT 2")
    #result = cursor.fetchall()
    #print((result))
        return render_template('index2.html', tDict = result)
    except:
        logging.exception("Webserver Fail") 
        print("Webserver Fail")
        return ("Web Failure")
        
if __name__ == "__main__":
    app.run(host='0.0.0.0')
    