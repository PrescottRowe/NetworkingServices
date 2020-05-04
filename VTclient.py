import json
import urllib2
import time
import csv

api_token = ''
api_url_base = 'https://www.virustotal.com/vtapi/v2/url/report?apikey='+ api_token

with open('covid_URLs_VT_lookup.csv') as csv_file:
    urlReader = csv.reader(csv_file, delimiter=',')
    for row in urlReader:
        searchUrl = ', '.join(row)
        get_report_url = api_url_base + '&resource='+ searchUrl
        request = urllib2.Request(get_report_url)
        response = urllib2.urlopen(request)
        data = json.load(response)
        try:
            print (searchUrl +" " + str(data["positives"]) + "/" + str(data["total"]))
        except:
            print (searchUrl + " ----won't scan-----")
        time.sleep(16)


