import pymysql
#uncomment the following line when you start project 3.2:
#from app import app


# Make sure you have data in your tables. You should have used auto increment for 
# primary keys, so all primary keys should start with 1

#you will need this helper function for all of your functions
#Use the uncommented version to test and turn in your code.  
#Comment out this version and then uncomment and use the second version below when you are importing 
#this file into your app.py in your I211_project for Project 3.2
def get_connection():
    return pymysql.connect(host="db.soic.indiana.edu",
                           user="i211s23_lsgulsen",
                           password="my+sql=i211s23_lsgulsen",
                           database="i211s23_lsgulsen", 
                           cursorclass=pymysql.cursors.DictCursor)

# def get_connection():
#     return pymysql.connect(host=app.config['DB_HOST'],
#                            user=app.config['DB_USER'],
#                            password=app.config['DB_PASS'],
#                            database=app.config['DB_DATABASE'],
#                            cursorclass=pymysql.cursors.DictCursor)

def get_trips():
    '''Returns a list of dictionaries representing all of the trips data'''
    conn = get_connection()
    trips = []
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM trips"
            cursor.execute(sql)
            trips = cursor.fetchall()
            return trips
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()

def get_trip(trip_id):
    '''Takes a trip_id, returns a single dictionary containing the data for the trip with that id'''
    conn = get_connection()
    trip = {}
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM trips WHERE trip_id=%s"
            cursor.execute(sql, (trip_id))
            trip = cursor.fetchone()
            return trip
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()

def add_trip(trip):
    '''Takes as input all of the data for a trip. Inserts a new trip into the trip table'''
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO trips (trip_name, level, start_date, location, length, leader, cost, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, trip)
            conn.commit()
            print("3. New trip added: " + str(trip) + "\n")
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()

def update_trip(trip_id, trip):
    '''Takes a trip_id and data for a trip. Updates the trip table with new data for the trip with trip_id as it's primary key'''
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE trips SET trip_name=%s, level=%s, start_date=%s, location=%s, length=%s, leader=%s, cost=%s, description=%s WHERE trip_id=%s"
            cursor.execute(sql, (trip['trip_name'], trip['level'], trip['start_date'], trip['location'], trip['length'], trip['leader'], trip['cost'], trip['description'], trip_id))
            conn.commit()
            print(f"4b. Trip with trip_id of {trip_id} updated to: {trip}\n")
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()

def add_member(member):
    '''Takes as input all of the data for a member and adds a new member to the member table'''
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO members (fname, lname, address, email, phone, dob) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, member)
            conn.commit()
            print("5. New member added: " + str(member) + "\n")
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()
    
def get_members():
    '''Returns a list of dictionaries representing all of the member data'''
    conn = get_connection()
    members = []
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM members"
            cursor.execute(sql)
            members = cursor.fetchall()
            return members
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()

def edit_member(member_id, member):
    '''Given an member__id and member info, updates the data for the member with the given member_id in the member table'''
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE members SET fname=%s, lname=%s, address=%s, email=%s, phone=%s, dob=%s WHERE member_id=%s"
            cursor.execute(sql, (member['fname'], member['lname'], member['address'], member['email'], member['phone'], member['dob'], member_id))
            conn.commit()
            print(f"7. Member with member_id of {member_id} updated to: {member}\n")
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()

def delete_member(member_id):
    '''Takes a member_id and deletes the member with that member_id from the member table'''
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM members WHERE member_id = %s"
            cursor.execute(sql, (member_id))
            conn.commit()
            print(f"8. Memmber with member_id of {member_id} deleted.\n")
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()
    
def add_member_trip(trip_id, member_id):
    '''Takes as input a trip_id and a member_id and inserts the appropriate data into the database that indicates the member with member_id as a primary key is attending the trip with the trip_id as a primary key'''
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO trip_members (trip_id, member_id) VALUES (%s, %s)"
            cursor.execute(sql, (trip_id, member_id))
            conn.commit()
            print(f"9. Member {member_id} added to the trip with trip_id of {trip_id}\n")
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()
    
def remove_member_trip(trip_id, member_id):
    '''Takes as input a trip_id and a member_id and deletes the data in the database that indicates that the member with member_id as a primary key 
    is attending the trip with trip_id as a primary key.'''
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM trip_members WHERE trip_id=%s AND member_id=%s"
            cursor.execute(sql, (trip_id, member_id))
            conn.commit()
            print(f"10. Member with member_id of {member_id} delete from attending trip with trip_id of {trip_id}.\n")
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()
    
def get_attendees(trip_id):
    '''Takes a t rip_id and returns a list of dictionaries representing all of the members attending the trip with trip_id as its primary key'''
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT m.member_id, m.fname, m.lname, m.address, m.email, m.phone, m.dob FROM trip_members tm JOIN members m ON tm.member_id = m.member_id WHERE tm.trip_id = %s"
            cursor.execute(sql, (trip_id))
            trips = cursor.fetchall()
            return trips
    except pymysql.err.ProgrammingError as ERROR:
        print("There was an error while executing the SQL query: '" + str(sql) + "'. Error: " + str(ERROR))
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    #add more test code here to make sure all your functions are working correctly
    try:
        #1
        # testing get_trips:
        print(f'1. All trips: {get_trips()}\n')


        # 2
        # testing get_trip:
        print(f'2. Trip info for trip_id 1: {get_trip(1)}\n')


        #3
        # testing add_trip:
        add_trip(("A Day in Yellowwood", "beginner", "2023-04-22", "Yellowwood State Forest", 1, "Sy Hikist", 10, "A day of hiking in Yellowwood. Bring a water bottle"))


        #4
        # testing update_trip WITH THE TRIP ADDED IN TEST CODE:
        trip_id = 7
        example_trip={"trip_name": "example trip name",
                           "level": "example level",
                           "start_date": "1999-01-01",
                           "location": "example location",
                           "length": 5,
                           "leader": "example name",
                           "cost": 20,
                           "description":"example description "}
        print(f"4a. Old trip info: {get_trip(trip_id)}\n")
        update_trip(trip_id, example_trip)


        #5
        # testing add_member
        add_member(("Tom", "Sawyer","101 E Sam Clemons Dr Bloomington, IN","tsawyer@twain.com", "812-905-1865","1970-04-01"))
        

        #6
        # testing get_members
        print(f'6. All Members: {get_members()}\n')


        #7
        # testing edit_member WITH THE MEMBER ADDED IN TEST CODE:
        member_id = 106
        example_member={"fname": "example",
                        "lname": "name",
                        "address": "123 Hello St",
                        "email": "example@email.com",
                        "phone": 888-888-8888,
                        "dob": "1999-01-01"}
        edit_member(member_id, example_member)


        #8
        # testing delete_member WITH THE MEMBER ADDED IN TEST CODE:
        member_id = 106
        delete_member(member_id)


        #9
        # testing add_member_trip:
        trip_id = 2
        member_id = 102
        add_member_trip(trip_id, member_id)


        #10
        # testing remove_member_trip WITH trip_members DATA ADDED IN TEST CODE ABOVE:
        # trip_id = 2
        # member_id = 102
        remove_member_trip(trip_id, member_id)


        #11
        # testing get_attendees
        print(f"11. All members attending the trip with trip_id 1: {get_attendees(1)}\n")
        
    except Exception as e:
        print(e)