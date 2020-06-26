import csv
import time
import requests
import json

api_token = ''#keys are $3.5 a month with a rate limit of 1.5 seconds (support says add 100 miliseconds to negate any 429 rate limits)
api_url_base = 'https://haveibeenpwned.com/api/v3' #line for url lookups
api_breached_account_path = "/breachedaccount/"
api_pastebin_path = "/pasteaccount/"
f = open('Compromised_creds.txt', 'w')
#point it at a csv file. file should have a header for each colum that is used for reference.
with open('lookup.csv') as csv_file:
    urlReader = csv.reader(csv_file, delimiter=',')

    s = str("Users who showed up in a breach:")
    f.write(s)
    for row in urlReader:
        searchUser = row[0]
        checkBreaches = api_url_base + api_breached_account_path + searchUser #build the full REST request
        checkPastes = api_url_base + api_pastebin_path + searchUser #
        #----------breach lookup---------
        response = requests.get(checkBreaches, headers={'hibp-api-key': api_token, 'User-Agent': 'python-requests/2.23.0' })
        if (response.status_code==429):
            time.sleep(1)
        if (response.status_code == 200):
            data = response.json()
            s = "\n" + searchUser
            f.write(s)
            s = str("\nBreaches:")
            f.write(s)
            for key in data:
                s = "\n\t"+ str(key['Name'])
                f.write(s)
        time.sleep(1.5)#Request throttling for

        #---------pastebin lookup---------
        response = requests.get(checkPastes, headers={'hibp-api-key': api_token, 'User-Agent': 'python-requests/2.23.0'})
        if (response.status_code==429):
            time.sleep(1)
        if (response.status_code == 200):
            data = response.json()  # parse
            s = str("\nPastes:")
            f.write(s)
            for key in data:
                s = "\n\t" + str(key['Source']) + " - " + str(key['Title']) + ", " + str(key['Date'])
                f.write(s)
        time.sleep(1.5)

    f.close()
    exit(0)

