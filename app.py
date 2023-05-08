#
# IMPORTS
#

from flask import Flask, render_template,  url_for, request, redirect
import csv, pymysql
from operator import itemgetter
from os.path import exists

app = Flask(__name__)

app.config.from_pyfile(app.root_path + '/config_defaults.py')
# setup config keys for database access
if exists(app.root_path + '/config.py'):
    app.config.from_pyfile(app.root_path + '/config.py')

# conn = pymysql.connect(
#     host=app.config['DB_HOST'],
#     user=app.config['DB_USER'],
#     password=app.config['DB_PASS'],
#     database=app.config['DB_DATABASE'],
#     cursorclass=pymysql.cursors.DictCursor)

import database



# 
# GLOBALS
#



TRIP_PATH = app.root_path + "/trips.csv"
MEMBER_PATH = app.root_path + "/members.csv"
TRIP_KEYS = ['name', 'start_date', 'length', 'location', 'level', 'leader', 'cost', 'description']
MEMBER_KEYS = ['name', 'address', 'email', 'dob','phone']

# 
# FUNCTIONS
#

# def get_trips():
#     results=[]
#     try:
#         with open(TRIP_PATH) as csv_file:
#             reader = csv.DictReader(csv_file)
#             results = list(reader)
#     except Exception as err:
#         print(err)
#     #return our data as a list of dictionaries
#     return results

# def set_trips(trips):
#     trips = sorted(trips, key=itemgetter('start_date'))
#     print(trips)
#     try:
#         with open(TRIP_PATH, mode='w', newline='') as csv_file:
#             writer = csv.DictWriter(csv_file, fieldnames=TRIP_KEYS)
#             writer.writeheader()
#             for trip in trips:
#                 writer.writerow(trip)
#     except Exception as err:
#         print(err)

# def get_members():
#     results=[]
#     try:
#         with open(MEMBER_PATH) as csv_file:
#             reader = csv.DictReader(csv_file)
#             results = list(reader)
#     except Exception as err:
#         print(err)
#     #return our data as a list of dictionaries
#     return results

# def set_members(members):
#     members= sorted(members, key=itemgetter('dob'))
#     try:
#         with open(MEMBER_PATH, mode='w', newline='') as csv_file:
#             writer = csv.DictWriter(csv_file, fieldnames=MEMBER_KEYS)
#             writer.writeheader()
#             for member in members:
#                 writer.writerow(member)
#     except Exception as err:
#         print(err)

def check_input_trip(trip_name, level, start_date, length, location, cost, leader, description):
    error = ""
    msg=[]
    if not trip_name:
        msg.append("Trip name is missing.")
    if len(trip_name) > 50:
        msg.append("Trip name is too long.")

    if not level:
        msg.append("Trip activity level is missing.")

    if not start_date:
        msg.append("Trip date is missing.")
    
    if not length:
        msg.append("Trip length is missing.")

    if not location:
        msg.append("Trip location is missing.")
    if len(location) > 50:
        msg.append("Trip location is too long.")

    if not cost:
        msg.append("Cost of trip is missing")
    if len(cost) > 4:
        msg.append("Cost of trip is too large.")

    if not leader:
        msg.append("Trip leader is missing.")
    if len(leader) > 40:
        msg.append("Trip leader name is too long.")

    if not description:
        msg.append("Trip description is missing.")
    if len(description) > 255:
        msg.append("Trip description is too long.")
    
    if not location:
        msg.append("Trip location")

    if len(msg) > 0:
        error = " \n".join(msg)
    
    return error

def check_input_member(fname, lname, address, email, dob, phone):
    error = ""
    msg=[]
    if not fname:
        msg.append("First name is missing.")
    if len(fname) > 20:
        msg.append("First name is too long.")
    
    if not lname:
        msg.append("Last name is missing.")
    if len(lname) > 20:
        msg.append("Last name is too long.")
    
    if not address:
        msg.append("Address is missing.")
    if len(address) > 50:
        msg.append("Address is too long.")
    
    if not email:
        msg.append("Email is missing.")
    if len(email) > 25:
        msg.append("Email is too long.")
    
    if not dob:
        msg.append("Date of birth is missing.")
    
    if not phone:
        msg.append("Phone number is missing.")
    if len(phone) > 12:
        msg.append("Phone number is too long.")

    if len(msg) > 0:
        error = " \n".join(msg)
    
    return error

#
# ROUTES
#

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trips/')
def list_trips():
    trips = database.get_trips()
    return render_template('trips.html', trips=trips)

@app.route('/members/')
def list_members():
    members = database.get_members()
    return render_template('members.html', members=members)

@app.route('/trips/<trip_id>/')
def view_trip(trip_id=None):
    if trip_id is not None:
        trip = database.get_trip(trip_id)
        if trip is not None:
            attendees = database.get_attendees(trip_id)
            not_attendees = database.get_not_attendees(trip_id)
            return render_template('trip.html', trip_id=trip_id, trip=trip, attendees=attendees, not_attendees=not_attendees)
        else:
            return redirect(url_for('list_trips'))
    else:
        return redirect(url_for('list_trips'))

@app.route('/trips/create', methods=['GET', 'POST'])
def create_trip():
    #if we have form data coming in via POST
    if request.method == 'POST':
        # grab the form data coming in
        trip_name = request.form['trip_name']
        level = request.form['level']
        start_date = request.form['start_date']
        length = request.form['length']
        location = request.form['location']
        cost = request.form['cost']
        leader = request.form['leader']
        description = request.form['description']

        error = check_input_trip(trip_name, level, start_date, length, location, cost, leader, description)
        if error:
            return render_template("trip_form.html", error=error, trip_name=trip_name, level=level, start_date=start_date, length=length, location=location, cost=cost, leader=leader, description=description)
        #add the new trip to the data
        new_trip=(trip_name, level, start_date, location, length, leader, cost, description)
        database.add_trip(new_trip)
        return redirect(url_for('list_trips'))
    else:
        return render_template('trip_form.html')
    
@app.route('/members/create', methods=['GET', 'POST'])
def create_member():
    #if we have form data coming in via POST
    if request.method == 'POST':
        # grab the form data coming in
        fname = request.form['fname']
        lname = request.form['lname']
        address = request.form['address']
        email = request.form['email']
        dob = request.form['dob']
        phone = request.form['phone']

        error = check_input_member(fname, lname, address, email, dob, phone)
        if error:
            return render_template("member_form.html", error=error, fname=fname, lname=lname, address=address, email=email, dob=dob, phone=phone)
        #add the new trip to the data
        new_member={'fname': fname, 'lname': lname, 'address':address, 'email': email, 'dob':dob,'phone':phone}
        database.add_member(new_member)
        # Return to the list of events.
        return redirect(url_for('list_members'))
    else:
        return render_template('member_form.html')

@app.route('/trips/<trip_id>/edit', methods=['GET', 'POST'])
def edit_trip(trip_id=None):
    trip_id = int(trip_id)
    #if we have form data coming in via POST
    if request.method== 'POST':
        # grab the form data coming in
        trip_name = request.form['trip_name']
        level = request.form['level']
        start_date = request.form['start_date']
        length = request.form['length']
        location = request.form['location']
        cost = request.form['cost']
        leader = request.form['leader']
        description = request.form['description']
        trip = {
            'trip_name': trip_name,
            'level': level,
            'start_date': start_date,
            'location': location,
            'length': length,
            'leader': leader,
            'cost': cost,
            'description': description
        }
        database.update_trip(trip_id, trip)
        #redirect to the trip page 
        return redirect(url_for('view_trip', trip_id=trip_id)) 
    else:
        #no form data, show the basic edit form with trip data passed in
        trip=database.get_trip(trip_id)
        return render_template('trip_form.html', trip_id=trip_id, trip=trip)
        
@app.route('/trip/<trip_id>/delete', methods=['GET', "POST"])
def delete_trip(trip_id=None):
    trip_id = int(trip_id)
    delete=request.args.get('delete', None)
    trip = database.get_trip(trip_id)
    attendees = []
    if delete == "1":
        attendees = database.get_attendees(trip_id)
        for attendee in attendees:
            database.remove_member_trip(trip_id, attendee['member_id'])
        database.delete_trip(trip_id)
        return redirect(url_for('list_trips'))  
    else:
        return render_template('delete_form.html', trip_id=trip_id, trip=trip, attendees=attendees)     

@app.route('/member/<member_id>/delete', methods=['GET', 'POST'])
def delete_member(member_id=None):
    member_id=int(member_id)
    delete=request.args.get('delete', None)
    member=database.get_member(member_id)
    if delete == "1":
        database.delete_member(member_id)
        return redirect(url_for('list_members'))
    else:
        return render_template('delete_member.html', member_id=member_id, member=member)
    
@app.route('/trips/<trip_id>/attendees/add', methods=['POST'])
def add_attendee(trip_id):
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        if member_id:
            database.add_member_trip(trip_id, member_id)
    return redirect(url_for('view_trip', trip_id=trip_id))

@app.route('/trips/<trip_id>/attendees/<member_id>/delete', methods=['POST'])
def delete_attendee(trip_id, member_id):
    database.remove_member_trip(trip_id, member_id)
    return redirect(url_for('view_trip', trip_id=trip_id))

#
# MAIN
#

if __name__ == '__main__':
    app.run(debug = True)