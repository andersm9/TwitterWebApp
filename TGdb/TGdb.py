import time
import subprocess
import requests
import pymysql.cursors
##wee test

## twitter credentials
from TwitterAPI import TwitterAPI
ACCESS_TOKEN_KEY = '493261235-o8QpxdHWHF9bjSklQDkHzybwIpQSfeWfFYu2Teuk'
ACCESS_TOKEN_SECRET = 'a2wxBz7flUHH2UP14z50ojbbORfqvXdUTxS1x7GoayXVu'
CONSUMER_KEY = 'WGPGfKozQ2kic5Hw9XgETlqaB'
CONSUMER_SECRET = 'cFzbRAg7R2RxReFd7nukCb1JdcCMKkCVKzePSArT7hKx5SInu1'
api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)
## Database


## google credentials
## requires env variable to be set as follows. this doesn't seem to work - need to manually execute the command::
#in  Dedian Dev: subprocess.Popen('export GOOGLE_APPLICATION_CREDENTIALS=/home/mark/Projects/Google/MAProject-5da8c0e41664.json', shell=True)
#in Production Ubuntu: export GOOGLE_APPLICATION_CREDENTIALS=/home/ubuntu/WebApp/TwitterWebApp/MAProject-5da8c0e41664.json
from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials

def google_geo(location):
    # Using Python requests and the Google Maps Geocoding API.
    #
    # References:
    # https://gist.github.com/pnavarrc/5379521
    # * http://docs.python-requests.org/en/latest/
    # * https://developers.google.com/maps/

    GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

    params = {
        'address': location,
    }
    # Make request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()

    # Use the first result
    result = res['results'][0]
    
    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']
    geodata['address'] = result['formatted_address']
    return (geodata['lat'],geodata['lng'])

## Google API section - takes a the text of a tweet (as text) and returns the polarity and magnitude (as text)
def google_sentiment(text):   
 DISCOVERY_URL = ('https://{api}.googleapis.com/'
                '$discovery/rest?version={apiVersion}')
 http = httplib2.Http()
 credentials = GoogleCredentials.get_application_default().create_scoped(
     ['https://www.googleapis.com/auth/cloud-platform'])
 http=httplib2.Http()
 credentials.authorize(http)
 service = discovery.build('language', 'v1beta1',
                           http=http, discoveryServiceUrl=DISCOVERY_URL)
 service_request = service.documents().analyzeSentiment(
   body={
     'document': {
        'type': 'PLAIN_TEXT',
        'content': text
     }
   })
 response = service_request.execute()
 polarity = response['documentSentiment']['polarity']
 magnitude = response['documentSentiment']['magnitude']
 print('Google 2 -Exit Sentiment: polarity of %s with magnitude of %s' % (polarity, magnitude))
 return (polarity, magnitude)


### Check location of tweet. These latitude and Longitude roughly equate to Scotland

def LocCck(lat,long):
    ##Scotland :
    if ((lat>55 and lat<61) and (long<-1.1 and long>-6.5)):
    #anywhere:
    #if ((lat>-200 and lat<200) and (long<200 and long>-200)):
        return True
    else:
        return False
    
### Twitter function. Obtains tweet details in a DICT with TRACK_TERM
### sends the text of the tweets to the google api function "main"

def Database_write2(tweet,polarity,magnitude, lat, long, user_name):
    # Open database connection
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='WebApp',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
    # Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO Gitter(TWEET,POLARITY, MAGNITUDE, LATITUDE, LONGITUDE, NAME) VALUES ('%s', '%d', '%f', '%f', '%f', '%s')" % \
       (tweet, polarity, magnitude, lat, long, user_name)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            connection.commit()
            print("DB Write complete")
        except:
            # Rollback in case there is any error
            connection.rollback()
            print("FAIL!!!!!    XXXXXXXXXXX        DB Write X - exception")
            return 
    connection.close()
## start here

if __name__ == "__main__":
    TRACK_TERM = 'Edinburgh'
    print("Twitter 1 - try to connect")
    r = api.request('statuses/filter', {'track': TRACK_TERM})
    print("connected, awaiting tweet")
    for item in r:
        print("new tweet ")
        #check language is english (some languages not supported by google sentiment API)
        if item['lang']=='en':
            user = item['user']
            try:
                #this will print out the tweet text:
                print(item['text'] if 'text' in item else item)
                #Prints out the users self defined location. Seems to e the most reliably filled fielf, though it's sometimes nonsence e.g. "The Moon" etc
                print("location = " + user['location'])
                #Attempts to convert the user location to latitude and longitude
                user_coord = google_geo(user['location'])
                print("coordinates = ")
                print(user_coord[0])
                print(user_coord[1])
                lat = user_coord[0]
                long = user_coord[1]
                #send the co-ords to check if they fit a predefined region
                Location_Check = LocCck(lat,long)
                #If the co-ords are within the predefined range, if so, normalise, guage sentiment and  and save to MySQL db
                if Location_Check==True:                   
                    print("username = ")
                    print(user['name'])
                    #check encoding is correct
                    tweet = item['text']
                    tweet2 = tweet.encode('utf-8')
                    tweet3=str(tweet2)
                    #remove key character " ' "
                    tweet4 = (tweet3.replace("'" , "" , 20))
                    #send tweet to google sentiment analysis
                    sentiment = google_sentiment(tweet4);
                    polarity = sentiment[0]
                    magnitude = sentiment[1]
                    #send the tweet, sentiment, co-ords and twitter username to the MySQL db
                    Database_write2(tweet4, polarity, magnitude, lat, long, user['name']);
                    print("------------------------------------------------------")
                else:
                    print("outside required location - break-----------------------")           
            except:
                print("not viable location")
                print("---------------------------------------")
        else:
            print("language not English------------------------------------")


    
    


        
    
        



