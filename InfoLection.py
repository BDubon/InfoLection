# The APIs
# InfoLection
# Last Revised: December 14, 2017

# Libraries Needed for the Program
import os
import json
import urllib.request
import urllib.parse
import urllib.error
from tkinter import *
from tkinter import ttk


# --- Dictionary Containing US State Abbreviations and its Corresponding Full Name ---
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
         }

# --- Function to make sure the user entered a valid year ---
# Written by Karyn, Ebrima, Bryan
def inputValidation(year):
    """ Takes the user input and makes sure that the year entered is within the
       accepted years by the API. If not, tells user to enter a valid year. """
    # Input validation
    year = int(year)  # Converting input to integer for comparison purposes
    userChoice = searchNum.get()
    if userChoice == 1:
        if 2003 <= year <= 2020:
            message = 'Here are the election dates requested for ' + str(year) + ':' + '\n'
        else:
            message = 'ERROR: Please enter a year between 2003-2020.\n\nYou entered ' + str(year)
    if userChoice == 2:
        if 1972 <= year <= 2020:
            message = 'Here are the candidates for ' + str(year) + ':' + '\n'
        else:
            message = 'ERROR: Please enter a year between 1976-2020.\n\nYou entered ' + str(year)

    # Clear out any existing text from entry window
    data.config(state=NORMAL)
    data.delete(0.0, END)
    # Set the data window
    data.insert(1.0, message)
    data.config(state=DISABLED)
    # Convert the year back to a string
    year = str(year)
    return year


# --- Function to get election dates data ---
# Provide a year between 2003-2020
# Written by Bryan
def apiCallDates(event, year, pageNumber):
    """ Requests data from OpenFEC API by constructing a url using predetermined
     values. Only produce data for years 2003-2020 as it's the only years
     available through the OpenFEC API. """

    apiKey = 'rdudHBjgS5srIohVWYyyUL64AOsqVfRkGZD4gvMU'
    perPage = '90'  # Number of items to print per page
    electionYear = year
    nullHide = 'true'
    nullOnly = 'true'
    # Sorting based on the user's selection in the GUI
    sort = sortNum.get()
    if sort == 1:
        sort = '-election_date'
    if sort == 2:
        sort = '-election_state'
    if sort == 3:
        sort = '-office_sought'
    # URL construction based on the user's input
    url = ('https://api.open.fec.gov/v1/election-dates/?per_page=' + perPage +
           '&api_key=' + apiKey +
           '&election_year=' + electionYear +
           '&page=' + pageNumber +
           '&sort_hide_null=' + nullHide +
           '&sort_null_only=' + nullOnly +
           '&sort=' + sort)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    js = json.loads(data)
    print(url)
    return js  # We receive a dictionary with all the info requested


# --- Function to print the API info ---
# Provide a year between 2003 - 2020
# Written by Bryan
def electionDates(event):
    """ Takes validated user input and requests data from OpenFEC API. Displays
       some predetermined information about election dates based on the year provided by the user. """
    year = yearEntry.get()  # User provided year
    year = inputValidation(year)
    pageNumber = '1'
    js = apiCallDates(event, year, pageNumber)  # Call the API by using the first function
    pages = js['pagination']['pages']           # Total number of pages
    print('TOTAL PAGES: ', pages)

    while int(pages) >= int(pageNumber):
        idx = 0
        totalItems = 0
        items = 0
        print('PAGE', pageNumber, 'OF', pages)
        for item in js['results']:
            state = js['results'][idx]['election_state']
            if state in states:
                state = state.replace(state, states[state])
            else:
                state = state
            date = js['results'][idx]['election_date']
            electionType = js['results'][idx]['election_type_full']
            notes = str(js['results'][idx]['election_notes'])
            office = js['results'][idx]['office_sought']
            # Changing initials from API to full office names
            if office == 'S':
                office = office.replace('S', 'Senate')  # Print out the full word instead of just the initial
            if office == 'H':
                office = office.replace('H', 'House of Representatives')  # Print out the full word, not the initial
            if office == 'P':
                office = office.replace('P', 'President')  # Print out the full word instead of just the initial
            idx = idx + 1  # idx allows us to iterate through each item in the dictionary

            # Displaying Data in Text Box
            data.config(state=NORMAL)

            data.insert(2.0, '' +
                        '\n' f'Date: {date}' +
                        '\n' f'State:  {state}' +
                        '\n' f'Election Type: {electionType}' +
                        '\n' f'Office: {office}' +
                        '\n' f'Notes: {notes}' +
                        '\n', '================')
            data.config(state=DISABLED)
            items = items + 1
        pageNumber = int(pageNumber) + 1
        pageNumber = str(pageNumber)
        js = apiCallDates(event, year, pageNumber)  # Re-call the API function to print the next page


# --- Function to Print Candidates' Information ---
# Provide any year
# Written by Kady and Bryan
def apiCallCandidates(event, year, pageNumber):
    """ Requests data from OpenFEC API by constructing a url using predetermined
     values. """
    electionYear = year
    apiKey = 'rdudHBjgS5srIohVWYyyUL64AOsqVfRkGZD4gvMU'
    perPage = '90'  # Number of items to print per page
    page = pageNumber
    sort = sortNum.get()
    if sort == 1:
        sort = '-name'
    if sort == 2:
        sort = '-state'
    if sort == 3:
        sort = '-office'
    url = ('https://api.open.fec.gov/v1/candidates/?&election_year=' + electionYear +
           '&api_key=' + apiKey +
           '&per_page=' + perPage +
           '&page=' + page +
           '&sort=' + sort)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    js = json.loads(data)
    print(url)
    return js


# --- Function to Print Candidates' Information ---
# Provide any year
# Written by Kady and Karyn
def candidatesInfo(event):
    """ This function lets us retrieve and display the data about candidates for a given year. """
    year = yearEntry.get()  # User provided year
    year = inputValidation(year)
    pageNumber = '1'
    js = apiCallCandidates(event, year, pageNumber)
    idx = 0
    pages = js['pagination']['pages']
    print('TOTAL PAGES: ', pages)
    print('')
    while int(pages) >= int(pageNumber):
        idx = 0
        items = 0
        print('PAGE', pageNumber, 'OF', pages)
        for item in js['results']:
            state = js['results'][idx]['state']
            if state in states:
                state = state.replace(state, states[state])
            else:
                state = state
            party = js['results'][idx]['party_full']
            name = js['results'][idx]['name']
            office = js['results'][idx]['office']
            # Changing initials from API to full office names
            if office == 'S':
                office = office.replace('S', 'Senate')  # Print out the full word instead of just the initial
            if office == 'H':
                office = office.replace('H', 'House of Representatives')  # Print out the full word, not the initial
            if office == 'P':
                office = office.replace('P', 'President')  # Print out the full wordq instead of just the initial
            incChallenge = js['results'][idx]['incumbent_challenge_full']
            cycles = js['results'][idx]['cycles']
            # Displaying Data in Text Box
            data.config(state=NORMAL)
            data.insert(2.0, '' +
                        '\n' f'Name: {name}' +
                        '\n' f'State:  {state}' +
                        '\n' f'Party: {party}' +
                        '\n' f'Office: {office}' +
                        '\n' f'Cycles: {cycles}' +
                        '\n', '')
            data.config(state=DISABLED)
            items = items + 1
            idx = idx + 1
        pageNumber = int(pageNumber) + 1
        pageNumber = str(pageNumber)
        js = apiCallCandidates(event, year, pageNumber)


# --- Submit button functionality ---
# Written by Bryan
def userSelection():
    """ This function lets us select which API we will use
    when the 'Submit' button is pressed. """
    userChoice = searchNum.get()
    if userChoice == 1:
        funcChoice = submitBtn.bind('<Button-1>', electionDates)
    if userChoice == 2:
        funcChoice = submitBtn.bind('<Button-1>', candidatesInfo)
    return funcChoice


# Written by Kady
def openAbout():
    """ This function opens a .txt file that contains information about our group and the project. """
    os.system('start " " InfoLection_About.txt')


# Written by Kady
def openInstruction():
    """ This function opens a .txt file that contains information and instructions
    about the program. """
    os.system('start " " InfoLection_READ_ME.txt')


        # -------- GUI CODE --------
# Designed by Karyn, Kady, Ebrima, Bryan
# Code written by Bryan

root = Tk()
root.title('InfoLection')
frame = Frame(root)
sortNum = IntVar()
searchNum = IntVar()
rmFile = "READ ME.txt"

# ---- Create label, button, entry and text widgets into our frame. ----
# --- Create instruction label ---
yearLbl = ttk.Label(root, text='Enter Year: ')
yearLbl.grid(row=0, column=0, sticky=E)

# --- Create Year Entry Box ---
yearEntry = ttk.Entry(root)
yearEntry.grid(row=0, column=1, columnspan=1, sticky=W)
yearEntry.delete(0, END)
yearEntry.insert(0, '')

# --- Create Submit Button ---
submitBtn = ttk.Button(root, text='Submit')
submitBtn.bind('<Button-1>', userSelection)
submitBtn.grid(row=3, column=0, columnspan=5, sticky=NSEW)

# Menu Bar
menu = Menu(root, tearoff=0)
root.config(menu=menu)
# Submenu
subMenu = Menu(menu)
menu.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label="Instructions", command=openInstruction)
subMenu.add_command(label="About", command=openAbout)
subMenu.add_command(label='Exit', command=root.quit)

# --- Radio Buttons For Different Functions ---
# Label
searchForLbl = ttk.Label(root, text='Search for: ')
searchForLbl.grid(row=1, column=0, sticky=E)
# Radio Buttons for Functions
datesRB = ttk.Radiobutton(root, text='Election Dates', command=userSelection, value=1, variable=searchNum)   # Search Election Dates
datesRB.grid(row=1, column=1, sticky=W)
candidatesRB = ttk.Radiobutton(root, text='Candidates', command=userSelection, value=2, variable=searchNum)  # Search Candidates' Information
candidatesRB.grid(row=1, column=2, sticky=W)

# --- Radio Buttons to Select Sorting Method ---
# Label
sortByLbl = ttk.Label(root, text='Sort by: ')
sortByLbl.grid(row=2, column=0, sticky=E)
# Radio Buttons
dateSortRB = ttk.Radiobutton(root, text='Date/Last Name', value=1, variable=sortNum)    # Sort by state
dateSortRB.grid(row=2, column=1, sticky=W)
stateSortRB = ttk.Radiobutton(root, text='State', value=2, variable=sortNum)      # Sort by date
stateSortRB.grid(row=2, column=2, sticky=W)
officeSortRB = ttk.Radiobutton(root, text='Office', value=3, variable=sortNum)  # Sort by Office
officeSortRB.grid(row=2, column=3, sticky=W)

# --- Text Widget To Display Data ---
data = Text(root, width=50, height=25, wrap=WORD)
data.grid(row=4, column=0, columnspan=4, sticky=NSEW)

# --- Scroll Bar ---
scroll = ttk.Scrollbar(root, command=data.yview)
data['yscrollcommand'] = scroll.set
scroll.grid(row=4, column=5, pady=3, sticky=NSEW)

# Window Icon
root.iconbitmap('InfoLectionIcon.ico')

# --- Keep Window Open ---
root.mainloop()



