'''
To do:
Build database parser to check that jobId doesnt already exist in database. (I don't want dubplicates)
Test for edge cases

'''
import sys
import pandas as pd

from datetime import date
from datetime import datetime
from datetime import timedelta
from time import sleep

from reed import Reed
from postgres import PostGresTools as pgtools

#These must be passed with the application initialisation
try:
    clientkey = sys.argv[1]
    dbkey = sys.argv[2]
except:
    print("The Reed API key and PostGreSQL database password must be passed with the program initialisation")
    sys.exit()

#Establish connection to both the API host and the locally hosted PostGreSQL database
Reed = Reed(key=clientkey)
pg = pgtools(dbname="jobSeeker", user="postgres",
             host="localhost", password=dbkey)

# if you want to send more locations to the API for results, add them to this list
#location = "Truro"
location = input('Please enter a city to search within: ')
loc_range = input('Within what range would you like me to search? (Miles): ')
#keywords to be fed into the search function
# keywords = ["Software", "Software engineer", "Graduate software"]
keywords = input('Please enter some keyphrases for me to search with, separated by a comma (,): ').split(",")

# Passed to an if statement as to whether the recent_jobs function is called
recent = input("Would you like just jobs posted in the last week? (Y/N): ").upper()

# Iterates over all the keywords supplied in the list 'keywords', returns all search data and appends to output
output = []
for keyword in keywords:
    tmp = {keyword: Reed.search(keywords=keyword,
                                locationName=location,
                                distanceFromLocation=loc_range)}
    output.append(tmp)

# Takes data from output list, iterates over each keyword search and commits to a the DataFrame object 'data'
columns = ['jobId', 'employerId', 'employerName', 'employerProfileId',
           'employerProfileName', 'jobTitle', 'locationName',
           'minimumSalary', 'maximumSalary', 'currency', 'expirationDate',
           'date', 'jobDescription', 'applications', 'jobUrl']
# creates a pandas DataFrame object, contains a None type row to hold structure
data = pd.DataFrame(index=[1], columns=columns)
for i in range(0, len(output)):  # Parses each keyword index in list
    for key in output[i].keys():  # Parses the keyword of the given index
        print("Searching '" + key + "'")
        # Iterates over each job entry returned by the api
        for values in output[i].values():
            # Temporarily stores converted json data
            tmp = Reed.json_to_pd(values)
            # Appends tmp data to empty DataFrame object
            data = data.append(tmp, ignore_index=True, sort=True)
            # Prints data from each job advert to user
            for k in list(values["results"]):
                print("    Returned: " +
                      str(k["jobTitle"] + " at " + str(k["employerName"])))
            print("Total results: " + str(values["totalResults"]))
        print("\n")

# Calls clean_cols function to remove jobs with None as jobId and removes unwanted columns before
# submission to SQL database
data = Reed.clean_cols(data)


# Calls recent_jobs function to remove jobs that were posted more than a week ago
# This keeps the data returned to a more reasonable scale in larger cities
if recent == 'Y':
    data = Reed.recent_jobs(data)
elif recent == 'N':
    pass
else:
    pass 
    #Need to build in an edge case exception here for typos


# Finally we want to push all the data to our database. Each new search will be stored in a new table to prevent overlaps.
table_name = "jobs_" + str(datetime.now())
pg.writeTable(data, table_name)
