##working from here:  https://github.com/PyMySQL/PyMySQL


from flask import Flask, render_template, request, json, Response
import pymysql.cursors

app = Flask(__name__)
mysql = MySQL(app)
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
                             cursorclass=pymysql.cursors.DictCursor)
@app.route("/")
def main():
##pyMySQL    
    with connection.cursor() as cursor:
    # Read a single record
        sql = "SELECT TWEET, POLARITY, MAGNITUDE, LATITUDE, LONGITUDE, NAME FROM Gitter ORDER BY MAGNITUDE DESC LIMIT 10"
        cursor.execute(sql)
        result = cursor.fetchall()
        print (type(result))
        print (result)
        #print ("   ")
    
#MySQL    
    #get the top 10 rows (by "MAGNITUDE") in the DB
    #cursor.execute("SELECT TWEET, POLARITY, MAGNITUDE, LATITUDE, LONGITUDE, NAME FROM Gitter ORDER BY MAGNITUDE DESC LIMIT 2")
    #result = cursor.fetchall()
    #print((result))
    return render_template('index2.html', tDict = result)
if __name__ == "__main__":
    app.run()
    