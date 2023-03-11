from flask import Flask, render_template, url_for, request, redirect
import csv

app = Flask(__name__)

# globals
TRIPS_PATH = app.root_path + '/trips.csv'
TRIPS_KEYS = ['Trip Name', 'Start Date', 'Length', 'Location', 'Level', 'Leader', 'Cost', 'Description']

MEM_PATH = app.root_path + '/members.csv'
MEM_KEYS = ['Name', 'DoB', 'Email', 'Address', 'Phone']

# functions from A7
    # takes data from trips.csv, returns a list of dictionaries, each dict is a trip

def get_trips():
    with open(TRIPS_PATH, 'r') as csvfile:
        data=csv.DictReader(csvfile)
        trips=list(data)
        return trips

    # takes a dictionary and saves it to csv
def set_trips(trip_list):
    with open(TRIPS_PATH, mode='w', newline='') as csvfile: # opening in 'w' because 'a' would just double data in file because in main, we are grabbing the list from the file in get_trips and appending new data
        # fieldnames = ['Trip Name', 'Start Date', 'Length', 'Location', 'Level', 'Leader', 'Cost', 'Description'] # need to set header row so it can add it again
        csvwriter = csv.DictWriter(csvfile, fieldnames=TRIPS_KEYS)
        csvwriter.writeheader() # need this because it deletes my header row when rewriting the file with the new list of appended data
        for trip in trip_list:
            csvwriter.writerow(trip) # rewriting the file with the new data
    pass

def get_members():
    with open(MEM_PATH, 'r') as csvfile: # only need to read to grab data 
        data = csv.DictReader(csvfile)
        members=list(data)
        return members
    
def set_members(member_list):
    with open(MEM_PATH, mode='w', newline='') as csvfile: # opening in 'w' because 'a' would just double data in file because in main, we are grabbing the list from the file in get_members and appending new data
        # fieldnames = ['Name', 'DoB', 'Email', 'Address', 'Phone'] # need to set header row so it can add it again
        csvwriter = csv.DictWriter(csvfile, fieldnames=MEM_KEYS)
        csvwriter.writeheader() # need this because it deletes my header row when rewriting the file with the new list of appended data
        for member in member_list:
            csvwriter.writerow(member) # rewriting the file with the new data
    pass

# routes

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/trips')
def trips():
    trips=get_trips()
    if not trips:
        return 'Error no trips' # error for my reference if failed
    return render_template('trips.html',trips=trips)
    
# creating links to each Trip Name iin 'trips.html' to a new page of details of specific trip
@app.route('/trips/<trip_id>')
def trip(trip_id):
    trips = get_trips() # using function above to get the data from trips
    for trip in trips:
        if trip['Trip Name'] == trip_id: 
            return render_template('trip.html', trip=trip)
    return 'Error trip not found' # error for my reference if failed

def get_oldest(member): # need to sort by oldest on top to youngest
    pass
@app.route('/members')
def members(m=None):
    members=get_members()
    if not members:
        return 'Error no members' # error for my reference if failed
    return render_template('members.html', members=members)