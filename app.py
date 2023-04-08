# 
# IMPORTS
#

from flask import Flask, render_template, url_for, request, redirect
import csv

app = Flask(__name__)

#
# GLOBALS
#

TRIPS_PATH = app.root_path + '/trips.csv'
TRIPS_KEYS = ['Trip Name', 'Start Date', 'Length', 'Location', 'Level', 'Leader', 'Cost', 'Description']

MEM_PATH = app.root_path + '/members.csv'
MEM_KEYS = ['Name', 'DoB', 'Email', 'Address', 'Phone']

#
# FUNCTIONS
#

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

# sorting members.csv so it is displayed in order of age
def sort_by_dob(member):
    # DoB in members.csv is MM/DD/YY and we are taking only those values
    dob = member['DoB'] # this is to still allow for sorting even with the dashes given with the input type "date" in add_member.html
    if '-' in dob:
        MM, DD, YY = [int(x) for x in dob.split('-')]
    else:
        MM, DD, YY = [int(x) for x in dob.split('/')]
    return YY, MM, DD # in the order of YY/MM/DD so it is sorted by the year, does not change MM/DD/YY order in csv file

# sorting trips.csv so it is displayed in order of date


#
# ROUTES
#

# homepage
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# trips
@app.route('/trips')
def trips():
    trips=get_trips()
    if not trips:
        return 'Error no trips' # error for my reference if failed
    return render_template('trips.html',trips=trips)
    
# creating links to each Trip Name in 'trips.html' to a new page of details of specific trip
@app.route('/trips/<trip_id>')
def trip(trip_id):
    trips = get_trips() # using function above to get the data from trips
    for trip in trips:
        if trip['Trip Name'] == trip_id: 
            return render_template('trip.html', trip=trip)
    return 'Error trip not found' # error for my reference if failed

@app.route('/edit_trip/<trip_id>', methods=['GET', 'POST'])
def edit_trip(trip_id):
    trips = get_trips()
    trip = None
    for t in trips:
        if t['Trip Name'] == trip_id:
            trip = t
            break

    if trip is None:
        return 'Error trip not found'

    if request.method == 'POST':
        for t in trips:
            if t['Trip Name'] == trip_id:
                t['Trip Name'] = request.form['trip_name']
                t['Start Date'] = request.form['start_date']
                t['Length'] = request.form['length']
                t['Location'] = request.form['location']
                t['Level'] = request.form['level']
                t['Leader'] = request.form['leader']
                t['Cost'] = request.form['cost']
                t['Description'] = request.form['description']


        set_trips(trips)
        
        # # using the type="date" in the input of Start Date in trips in add_trip.html, the form takes the date as YYYY-MM-DD, so i need to convert it to MM/DD/YY for my csv file.
        # date = request.form['start_date']
        # YYYY, MM, DD = date.split('-')
        # # convert to MM/DD/YY
        # date_convert = '{}/{}/{}'.format(MM, DD, YYYY[2:]) # this 2 takes away the first 2 numbers in the YEAR of YYYY/MM/DD ex: 1982 >> 82
        # trip['Start Date'] = date_convert
        # set_trips(trips)

        # # adding member to the trips.csv
        # with open('trips.csv', mode='a') as csv_file:
        #     writer = csv.DictWriter(csv_file, fieldnames=trip.keys())
        #      # make sure it converts the date when adding to CSV
        #     writer.writerow(trip)
        
        return redirect(url_for('trip', trip_id=trip['Trip Name']))
    
    return render_template('edit_trip.html', trip=trip)

@app.route('/delete_trip/<trip_id>')
def delete_trip(trip_id):
    trips = get_trips() # using function above to get the data from trips
    for trip in trips:
        if trip['Trip Name'] == trip_id: 
            return render_template('delete_trip.html', trip=trip)
    return 'Error trip not found' # error for my reference if failed

@app.route('/confirm_delete_trip/<trip_id>', methods=['POST'])
def confirm_delete_trip(trip_id):
    trips = get_trips()
    find_trip = False
    for trip in trips:
        if trip['Trip Name'] == trip_id:
            trips.remove(trip)
            find_trip = True
            break

    if find_trip:
        set_trips(trips)
        return redirect('/trips')
    else:
        return 'Error trip not found'


# members
@app.route('/members')
def members(m=None):
    members=get_members()
    if not members:
        return 'Error no members' # error for my reference if failed
    # now taking sort_by_dob() to sort the members.csv
    members.sort(key=sort_by_dob)
    return render_template('members.html', members=members)

# add a member
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        member = {
            'Name': request.form['name'],
            'DoB': request.form['dob'],
            'Email': request.form['email'],
            'Address': request.form['address'],
            'Phone': request.form['phone']
        }

        # using the type="date" in the input of DoB in members in add_member.html, the form takes the date as YYYY-MM-DD, so i need to convert it to MM/DD/YY for my csv file.
        dob = request.form['dob']
        YYYY, MM, DD = dob.split('-')
        # convert to MM/DD/YY
        dob_convert = '{}/{}/{}'.format(MM, DD, YYYY[2:]) # this 2 takes away the first 2 numbers in the YEAR of YYYY/MM/DD ex: 1982 >> 82

        # adding member to the members.csv
        with open('members.csv', mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=member.keys())
            member['DoB'] = dob_convert # make sure it converts the DoB when adding to CSV
            writer.writerow(member)

        return redirect(url_for('members'))
    else:
        return render_template('add_member.html')
    
@app.route('/add_trip', methods=['GET', 'POST'])
def add_trip():
    if request.method == 'POST':
        trip = {
            'Trip Name': request.form['trip_name'],
            'Start Date': request.form['start_date'],
            'Length': request.form['length'],
            'Location': request.form['location'],
            'Level': request.form['level'],
            'Leader': request.form['leader'],
            'Cost': request.form['cost'],
            'Description': request.form['description']
        }

        # # using the type="date" in the input of Start Date in trips in add_trip.html, the form takes the date as YYYY-MM-DD, so i need to convert it to MM/DD/YY for my csv file.
        # date = request.form['start_date']
        # YYYY, MM, DD = date.split('-')
        # # convert to MM/DD/YY
        # date_convert = '{}/{}/{}'.format(MM, DD, YYYY[2:]) # this 2 takes away the first 2 numbers in the YEAR of YYYY/MM/DD ex: 1982 >> 82

        # adding member to the trips.csv
        with open('trips.csv', mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=trip.keys())
            writer.writerow(trip)

        return redirect(url_for('trips'))
    else:
        return render_template('add_trip.html')