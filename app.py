from flask import Flask, render_template,  url_for, request, redirect
import csv
from operator import itemgetter

app = Flask(__name__)

TRIP_PATH = app.root_path + "/trips.csv"
MEMBER_PATH = app.root_path + "/members.csv"
TRIP_KEYS = ['name', 'start_date', 'length', 'location', 'level', 'leader', 'cost', 'description']
MEMBER_KEYS = ['name', 'address', 'email', 'dob','phone']

def get_trips():
    results=[]
    try:
        with open(TRIP_PATH) as csv_file:
            reader = csv.DictReader(csv_file)
            results = list(reader)
    except Exception as err:
        print(err)
    #return our data as a list of dictionaries
    return results

def set_trips(trips):
    trips = sorted(trips, key=itemgetter('start_date'))
    print(trips)
    try:
        with open(TRIP_PATH, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=TRIP_KEYS)
            writer.writeheader()
            for trip in trips:
                writer.writerow(trip)
    except Exception as err:
        print(err)

def get_members():
    results=[]
    try:
        with open(MEMBER_PATH) as csv_file:
            reader = csv.DictReader(csv_file)
            results = list(reader)
    except Exception as err:
        print(err)
    #return our data as a list of dictionaries
    return results

def set_members(members):
    members= sorted(members, key=itemgetter('dob'))
    try:
        with open(MEMBER_PATH, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=MEMBER_KEYS)
            writer.writeheader()
            for member in members:
                writer.writerow(member)
    except Exception as err:
        print(err)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trips/')
def list_trips():
    trips = get_trips()
    return render_template('trips.html', trips=trips)

@app.route('/members/')
def list_members():
    members = get_members()
    return render_template('members.html', members=members)

@app.route('/trips/<trip_id>/')
def view_trip(trip_id=None):
    if trip_id:
        #grab trip_id from route and convert to int so we can use it as an index
        trip_id = int(trip_id)
        trips=get_trips()
        trip = trips[trip_id]
        return render_template('trip.html', trip_id=trip_id, trip=trip)
    else:
        return redirect(url_for('list_trips'))

@app.route('/trips/create', methods=['GET', 'POST'])
def create_trip():
    #if we have form data coming in via POST
    if request.method == 'POST':
        # grab the form data coming in
        name = request.form['name']
        level = request.form['level']
        start_date = request.form['start_date']
        length = request.form['length']
        location = request.form['location']
        cost = request.form['cost']
        leader = request.form['leader']
        description = request.form['description']
        #add the new trip to the data
        trips=get_trips()
        new_trip={'name':name, 'level':level, 'start_date':start_date, 'length':length, 'location':location, 'cost':cost, 'leader':leader, 'description':description}
        trips.append(new_trip)
        set_trips(trips)
        # Return to the list of events.
        return redirect(url_for('list_trips'))
    else:
        return render_template('trip_form.html')
    
@app.route('/members/create', methods=['GET', 'POST'])
def create_member():
    #if we have form data coming in via POST
    if request.method == 'POST':
        # grab the form data coming in
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        dob = request.form['dob']
        phone = request.form['phone']
        #add the new trip to the data
        members=get_members()
        new_member={'name': name, 'address':address, 'email': email, 'dob':dob,'phone':phone}
        members.append(new_member)
        set_members(members)
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
        name = request.form['name']
        level = request.form['level']
        start_date = request.form['start_date']
        length = request.form['length']
        location = request.form['location']
        cost = request.form['cost']
        leader = request.form['leader']
        description = request.form['description']
        #save the modified trips to the data
        trips=get_trips()
        new_trip={'name':name, 'level':level, 'start_date':start_date, 'length':length, 'location':location, 'cost':cost, 'leader':leader, 'description':description}
        trips[trip_id]=new_trip
        set_trips(trips)
        #redirect to the trip page 
        return redirect(url_for('view_trip', trip_id=trip_id)) 
    else:
        #no form data, show the basic edit form with trip data passed in
        trips=get_trips()
        trip=trips[trip_id]
        return render_template('trip_form.html', trip_id=trip_id, trip=trip)
        
@app.route('/trip/<trip_id>/delete', methods=['GET', "POST"])
def delete_trip(trip_id=None):
    trip_id = int(trip_id)
    delete=request.args.get('delete', None)
    trips=get_trips()
    trip=trips[trip_id]
    if delete == "1":
        del trips[trip_id]
        set_trips(trips)
        return redirect(url_for('list_trips'))  
    else:
        return render_template('delete_form.html', trip_id=trip_id, trip=trip)      



if __name__ == '__main__':
    app.run(debug = True)