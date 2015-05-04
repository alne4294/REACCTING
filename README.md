# DataEng_hmwk5

Tyler Bussell, Alexia Newgord, Justin McBride, David Baird

#### To access exisiting application

```
cd App
python app.py
```

You can view the app by going to http://localhost:5000/animation.  It should look like this:

![alt tag](screenshot1.png)

It may ask for authentication, which in the code, it's clearly just Username: reaccting and Password: ghana

I'm guessing you're lacking dependencies.  I have a lot of the dependencies listed in the requirements.txt, so I recommend issuing the following command:

```
pip install -r requirements.txt
```

I'm not sure what I'm missing from there, but it should be pretty clear in the console error messsages.  Feel free to add to it if that seems appropriate.  There might be some javascript packages that I installed via NPM that you would need too... sorry, I'm not sure how to check what is "global" and what I included in this directory.

The framework for accessing data from a MongoDB is already in the app.py (see index.html at http://localhost:5000).  I'm working on changing the SUMs dataset access to PEMs.  Details to come for that.  I'll probably just create an export of the database for you to use since MongoLab isn't cheap.

Here's a screenshot of what the current mongo framework does, since it won't show on yours because you don't have the SUMs database:

![alt tag](screenshot2.png)

#### About the PEMs Data

The Personal Emissions Monitor data (PEMs) records the emissions associated with a 1-2 hour cooking "event".  So, basically, once a day, the Ghana workers put this tracking device over the cookstove and the results are recorded. The spreadsheets in  PEMs_data/ComparingAcrossStovesAndSeasons.xlsx says what time is associated with which device etc.  In the interest of time, it may be easiest to convert this into a lookup data structure (json, dict, etc.) on either the frontend or backend rather than trying to parse it.

There are four different kinds of cookstoves that are being compared.  See http://www.reaccting.com/pictures/ for pics of the study.

We're trying to see how patterns of CO2/NO2/etc. intake relates to geographic location and possibly other variables (population, wealth, weather, etc.), time permitting.  So basically, we can just plug this in visually to the existing map and hope that it provides some insight.

#### To import the PEMs database

```
mongorestore --collection p1 --db pems PEMs_data/dump/pems/p1.bson
```

It's less than a gig and should have 6343 records.
