#Handles REST requests for accessing REACCTING data in MongoDB

import pymongo
from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify, Response
from functools import wraps
import json
from bson import json_util
import os

from parseData import parseWorkbook

app = Flask(__name__)

#==========================================================
#Formats error response to JSON

def format_error(message):
    return jsonify(error=1, data=message)


#==========================================================
#Authentication helpers

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid."""
    return True
    # return username == 'reaccting' and password == 'ghana'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


#==========================================================
#GET

@app.route('/api/1.0/mongoWebApp/find', methods=['GET'])
@requires_auth
def find():
  try:
    conn=pymongo.MongoClient(host='localhost',port=27017)
    PEMsDB = conn['pems'] # Load the 'pems' database
    print "Connected to: " + str(PEMsDB)
  except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e 

  collection = PEMsDB['p1']

  docs = collection.find().sort([('iso_date', pymongo.ASCENDING)])

  json_docs = []
  for doc in docs:
    json_doc = json.dumps(doc, default=json_util.default)
    json_docs.append(json_doc)

  return jsonify(error=0, data=json_docs)

@app.route('/api/1.0/mongoWebApp/create', methods = ['POST', 'PUT'])
@requires_auth
def create():
  if request.method == 'POST':
    try:
      conn = pymongo.MongoClient(host = 'localhost', port = 27017)
      PEMsDB = conn['pems']
      print "Connect to: " + str(PEMsDB)
    except pymongo.errors.ConnectionFailure, e:
      print "Could not connect to MongoDB: %s" % e

    collection = PEMsDB['p1']

    print "GOOD"
    data = request.get_json(force=True)
    id_added = collection.insert_one(data).inserted_id
    print "GOODER"

    return jsonify(id = str(id_added))

@app.route('/api/1.0/mongoWebApp/delete/<int:day>', methods=['GET'])
@requires_auth
def deleteData( day ):
  try:
    conn=pymongo.MongoClient(host='localhost',port=27017)
    PEMsDB = conn['pems'] # Load the 'pems' database
    print "Connected to: " + str(PEMsDB)
  except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e
    return
  collection = PEMsDB['p1']
  rv = collection.delete_many({'day': day})
  num = rv.deleted_count
  return jsonify(numberDeleted=num)

@app.route( '/api/1.0/mongoWebApp/getHouseholdData' )
@requires_auth
def getHouseholdData():
  # Open the file for reading
  jsonFile = open('householdData.json', 'r')

  # Load the contents from the file, which creates a new dictionary
  householdDict = json.load(jsonFile)

  # Close the file... we don't need it anymore  
  jsonFile.close()

  return jsonify(data=householdDict)

@app.route('/api/1.0/mongoWebApp/getPemsHouseholdData')
@requires_auth
def getPemsHouseholdData():
  jsonFile = open( 'stoves.json', 'r' );
  objs = json.load( jsonFile )

  jsonFile.close()

  return jsonify( data=objs )

@app.route('/api/1.0/mongoWebApp/getPhoneData/<int:phoneNum>')
@requires_auth
def getPhoneData(phoneNum):
  
  if(phoneNum < 1 or phoneNum > 2):
    # Return empty dictionary
    return jsonify(data={})
  

  # Open the file for reading
  jsonFile = open('Phone'+str(phoneNum)+'.json', 'r')

  # Load the contents from the file, which creates a new dictionary
  coordDict = json.load(jsonFile)

  # Close the file... we don't need it anymore  
  jsonFile.close()

  week   = ['Sunday', 
          'Monday', 
          'Tuesday', 
          'Wednesday', 
          'Thursday',  
          'Friday', 
          'Saturday']

  # Convert Matlab time into Gregorian time string
  for doc in coordDict:
    temp = doc["time"];
    matlab_datenum = float(doc["time"])
    python_datetime = datetime.fromordinal(int(matlab_datenum)) + timedelta(days=matlab_datenum%1) - timedelta(days = 366)
    #Convert to string and remove units smaller than seconds
    weekday = python_datetime.weekday()
    dateAndTime = (str(python_datetime)).split('.', 1)[0]
    doc["date"], doc["time"] = dateAndTime.split(' ', 1)
    doc["date"] = week[weekday] + ", " + doc["date"]
    # print temp + " " + doc["date"] + " - " + doc["time"]

  return jsonify(data=coordDict)

@app.route('/pemsAnimation')
@requires_auth
def pemsanimation():
    return render_template('pemsAnimation.html')

@app.route('/animation')
@requires_auth
def animation():
    return render_template('animation.html')

@app.route('/dataDocumentation')
@requires_auth
def dataDocumentation():
    return render_template('dataDocumentation.html')

@app.route('/howToUse')
@requires_auth
def howToUse():
    return render_template('howToUse.html')

@app.route("/")
@requires_auth
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
