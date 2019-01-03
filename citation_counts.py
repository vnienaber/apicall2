import requests
import time
import json
import csv
import random

filestring = 'results_200000.csv'

def dslquery(query, retries=0):


    jsonresult = {}
    api_url = 'https://api.elsevier.com/content/abstract/citations?doi=ADD_DOI&date=2015-2018&apiKey=3c7e910363450b6a1e26ed6181a4593f&httpAccept=application%2Fjson'
    doi = query
    api_url = api_url.replace("ADD_DOI", str(doi))
    result = requests.post(api_url,data=query)
    last_dsl_query = time.time()

    try:
        jsonresult = json.loads(result.text)
        #print jsonresult
    except:
        if retries < 1:
            # The Dimensions API is limited to 1 query every 30 seconds
            time.sleep(max([0, 2 - (time.time() - last_dsl_query)]))
            retries = retries + 1
            jsonresult = dslquery(query, retries)
        else:
            if result.status_code != 200: print('SN Insights response error ' + str(result.status_code))
            if result.text == u'[]': print('SN Insights empty response')
            jsonresult = {"error": result.text}
            print (jsonresult)
    try:
        citeCountHeader = jsonresult['abstract-citations-response']['citeColumnTotalXML']['citeCountHeader']
        doi_list = []
        for doi in  jsonresult['abstract-citations-response']['identifier-legend']['identifier'][:1]:
            doi = doi['prism:doi']
            doi_list.append(doi)
        return_stuff(doi_list, citeCountHeader)

    except:
        print 'Error for doi ' + str(doi)
        with open('error', mode='a') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # csv_writer.writerow(['doi', 'ms_title', 'pubdate', 'subjects'])
            csv_writer.writerow([doi])
        pass






def return_stuff(doi, citeCountHeader):
    try:
        heading = citeCountHeader['columnHeading']
    except:
        heading = None
    try:
        total = citeCountHeader['columnTotal']
    except:
        total = None
    try:
        gtotal = citeCountHeader['grandTotal']
    except:
        gtotal = None
    try:
        later = citeCountHeader['laterColumnTotal']
    except:
        later = None
    try:
        previous =  citeCountHeader['prevColumnTotal']
    except:
        previous = None

    with open(filestring, mode='a') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # csv_writer.writerow(['doi', 'ms_title', 'pubdate', 'subjects'])
        csv_writer.writerow([doi[0], total[0]["$"],total[1]["$"],total[2]["$"], total[3]["$"],previous, later, gtotal])


dois = ['10.1016/S0014-5793(01)03313-0', '10.1034/j.1399-3011.2002.21003.x']

with open('dois.txt') as f:
    fdata = [line.rstrip() for line in f]
f = fdata[100000:200000]
#print f

start= time.time()
with open(filestring, mode='w') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['doi', '2015', '2016', '2017', '2018', 'previous', 'later', 'total'])
for i in f:
    dslquery(i)
end = time.time()

print end-start
