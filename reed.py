'''
This file is just for establishing what the Reed api will return when called. 
Reed is a job search platform that offers a free developer API. I'll make use of that API for job hunting

Haven't managed to find any documentation on API call limits, but have encountered a call refusal once during testing.

Access format: https://www.reed.co.uk/api/{version number}/jobs/{Job Id} 
e.g. https://www.reed.co.uk/api/1.0/jobs/132
Search format: https://www.reed.co.uk/api/{versionnumber}/search?keywords={keywords}
                &locationName={locationName}&employerId={employerId}
                &distanceFromLocation={distanceinmiles}'

API returns a list of dictionaries, one for each job. The returned job data is given as:
{'employerId': 0,
 'employerName': None,
 'jobId': 0,
 'jobTitle': None,
 'locationName': None,
 'minimumSalary': None,
 'maximumSalary': None,
 'yearlyMinimumSalary': None,
 'yearlyMaximumSalary': None,
 'currency': None,
 'salaryType': None,
 'salary': None,
 'datePosted': None,
 'expirationDate': None,
 'externalUrl': None,
 'jobUrl': None,
 'partTime': False,
 'fullTime': False,
 'contractType': None,
 'jobDescription': None,
 'applicationCount': 0}

Documentation
https://www.reed.co.uk/developers/Jobseeker
'''

import requests
import json
import pandas as pd
from datetime import datetime

class Reed():
    def __init__(self, key):
        self.key = key
        try:
            requests.get("https://www.reed.co.uk/api/1.0/jobs/132", auth = (self.key,"")) #need to update test
            print('\nAPI connection established\n')
        except:
            print("API connection not established, please provide a valid API key")

    def build_url(self, params):
        '''
        Builds the URL for the search function based on passed parameters
        Format of search url:
        https://www.reed.co.uk/api/{versionnumber}/search?keywords={keywords}
        &locationName={locationName}&employerId={employerId}&distanceFromLocation=
        {distance in miles}
        '''
        output = ''
        for key, value in params.items():
            if value is not '':
                output = output + '&' + key + '=' + value
        c = "https://www.reed.co.uk/api/1.0/search?"
        url = c + output
        return url

    def search(self, **kwargs):
        '''
        Returns data from Reed API
        '''

        #parameters used by the API, these are injected into the build_url function
        params = {
            'keywords': kwargs.get('keywords', ''),
            'locationName': kwargs.get('locationName', ''),
            'employerId': kwargs.get('employerId', ''),
            'distanceFromLocation': kwargs.get('distanceFromLocation', '')
        }
        url = self.build_url(params)
        response = requests.get(url, auth=(self.key, ""))

        try:
            data = json.loads(response.text)
        except ValueError:
            print("No job found")
            #print("No new '{}' jobs were found in {}".format(params["keywords"],
            #                                                 params["locationName"]
            #                                                 ))
            print("\n\n")
            data = None
        return data

    def json_to_pd(self, data):
        return pd.DataFrame(data["results"])

    def clean_cols(self, data):
        del_cols = ["currency", "employerId",
                    "employerProfileId", "employerProfileName"]
        for col in del_cols:
            data = data.drop(col, 1)
        # Removes any NoneType jobs. Jobs must have a jobId.
        data = data.dropna(subset=['jobId'])
        return data
    
    def recent_jobs(self, data):
        recent_data = data
        for index in data.itertuples():
            if (datetime.today() - datetime.strptime(str(index[2]), '%d/%m/%Y')).days > 7:
                recent_data = recent_data.drop(index[0])
        return recent_data
