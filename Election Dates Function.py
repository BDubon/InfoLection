# Last Revised: November 28, 2017

import json
import urllib.request, urllib.parse, urllib.error


# Function to call the API
def apiCall(year, pageNumber):
    """ Requests data from OpenFEC API by constructing a url using predetermined
     values. """
    apiKey = 'rdudHBjgS5srIohVWYyyUL64AOsqVfRkGZD4gvMU'
    perPage = '25'              # Number of items to print per page
    electionYear = year
    sort = 'election_date'
    url = ('https://api.open.fec.gov/v1/election-dates/?per_page=' + perPage +
           '&api_key=' + apiKey +
           '&election_year=' + electionYear +
           '&page=' + pageNumber +
           '&sort=' + sort)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    js = json.loads(data)

    return js                   # We receive a dictionary with all the info requested

# Function to print the API info
# Provide a year between 2003 - 2020
def electionDates(years):
    year = str(years)
    pageNumber = '1'
    js = apiCall(year, pageNumber)    # Call the API by using the first function
    pages = js['pagination']['pages']
    print('TOTAL PAGES: ', pages)
    #print('TOTAL ITEMS: ', items)
    while int(pages) >= int(pageNumber):
        idx = 0
        items = 0
        print('PAGE', pageNumber, 'OF', pages)
        for item in js['results']:
            state = js['results'][idx]['election_state']
            date = js['results'][idx]['election_date']
            electionType = js['results'][idx]['election_type_full']
            notes = js['results'][idx]['election_notes']
            office = js['results'][idx]['office_sought']
            if office == 'S':
                office = office.replace('S', 'Senate')         # Print out the full word instead of just the initial
            if office == 'H':
                office = office.replace('H', 'House')          # Print out the full word instead of just the initial
            if office == 'P':
                office = office.replace('P', 'President')      # Print out the full word instead of just the initial
            idx = idx + 1                             # idx allows us to iterate through each item in the dictionary
            print('State:', state, '|',               # We can add or remove as many of these as we want
                  'Date:', date, '|',
                  'Election Type:', electionType, '|',
                  'Office:', office, '|',
                  'Notes:', notes,)
            items = items + 1
        print('TOTAL ITEMS:', items)
        print('---------------------------------------------------------------------------------------------------')
        pageNumber = int(pageNumber) + 1
        pageNumber = str(pageNumber)
        js = apiCall(year, pageNumber)                # Re-call the API function to print the next page





# Provide a year between 2003 - 2020
userYear = input('Please enter a year: ')
electionDates(userYear)

