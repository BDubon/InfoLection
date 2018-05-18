import json
import urllib.request, urllib.parse, urllib.error
from tkinter import *
import tkinter.messagebox

def apiCall(year, pageNumber):
    """ Requests data from OpenFEC API by constructing a url using predetermined
     values. """
    apiKey = 'rdudHBjgS5srIohVWYyyUL64AOsqVfRkGZD4gvMU'
    perPage = '25'              # Number of items to print per page
    electionYear = year
    page = pageNumber
    url = ('https://api.open.fec.gov/v1/candidates/?year=' + electionYear +
            '&has_raised_funds=true' 
            '&election_year=' + electionYear +
            '&api_key=' + apiKey +
            '&per_page=' + perPage +
            '&page=' + page +
            '&sort=name')
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    js = json.loads(data)
    print(url)
    return js

def candidatesInfo():
    year = '2017'
    pageNumber = '1'
    js = apiCall(year, pageNumber)
    idx = 0
    pages = js['pagination']['pages']
    print('TOTAL PAGES: ', pages)
    print('')
    while int(pages) >= int(pageNumber):
        idx = 0
        items = 0
        print('PAGE', pageNumber, 'OF', pages)
        parties = []
        demsList = []
        repList = []
        democrats = 0
        demsTotal = 0
        republicans = 0
        repTotal = 0
        other = 0
        for item in js['results']:
            party = js['results'][idx]['party_full']
            name = js['results'][idx]['name']
            if party not in parties:
                parties.append(party)
            else:
                partyTotal = 0
            if party == "DEM":
                demsList.append(name)
            items = items + 1
        print(parties)
        print(demsList)
        demsTotal = democrats + demsTotal
        print('DEMS: ', democrats)
        print('REPS: ', republicans)
        print('OTHER: ', other)
        print('demstotal: ', demsTotal)
        print('TOTAL ITEMS:', items)
        pageNumber = int(pageNumber) + 1
        pageNumber = str(pageNumber)
        js = apiCall(year, pageNumber)


apiCall('2016', '1')