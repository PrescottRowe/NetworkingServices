import json
import urllib2
import time
import csv

api_token = ''#get a free token
api_url_base = 'https://www.virustotal.com/vtapi/v2/url/report?apikey='+ api_token #line for url lookups
#point it as a csv file. file should have a header for each colum that is used for reference.
with open('lookup.csv') as csv_file:
    urlReader = csv.reader(csv_file, delimiter=',')
    for row in urlReader:
        searchUrl = ', '.join(row)
        get_report_url = api_url_base + '&resource='+ searchUrl #build the full REST request
        request = urllib2.Request(get_report_url)
        response = urllib2.urlopen(request) #send request and get response
        data = json.load(response) #parse
        try:
            print (searchUrl +" " + str(data["positives"]) + "/" + str(data["total"]))
        except:
            print (searchUrl + " ----won't scan-----")
        time.sleep(16)


