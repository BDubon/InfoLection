import json
import urllib.request, urllib.parse, urllib.error
from tkinter import *
from tkinter import ttk
import tkinter.messagebox


# Define the GUI Application
class InfoLection(Frame):
    """ GUI App -> Provide election information. """
    # Constructor Method (AKA Initializer)
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()


    def create_widgets(self):
        """ Create label, button, entry and text widgets into our frame. """
        # Create instruction label
        self.year_lbl = ttk.Label(self,text='Enter Year: ')
        self.year_lbl.grid(row=0, column=0, sticky=E)

        # Create Entry Box
        self.year_entry = ttk.Entry(self)
        self.year_entry.grid(row=0, column=1, columnspan=2, sticky=W)

        # Create Submit Button
        self.submit_btn = ttk.Button(self, text='Submit', command=self.Data)
        self.submit_btn.grid(row=1, column=0, columnspan=3, sticky=NSEW)

        # Text Widget To Display Data
        self.data = Text(self, width=50, height=50, wrap=WORD)
        self.data.grid(row=2, column=0, columnspan=3, sticky=NSEW)

    def Data(self):
        # Ask the user for a year
        year = self.year_entry.get()
        # Input validation
        year = int(year) # Converting input to integer for comparison purposes
        if year >= 2003 and year <= 2020:
            message = "Here's the data you requested!"
        else:
            message = "Please enter a valid year."
        # Clear out any existing text from entry window
        self.data.delete(0.0, END)
        # Set the data window
        self.data.insert(0.0, message)
        # Convert the year back to a string
        year = str(year)
        return year

# Main
root = Tk()
root.title('InfoLection')
root.geometry('405x400')

# Create object (Initialize)
app = InfoLection(root)
root.mainloop()

