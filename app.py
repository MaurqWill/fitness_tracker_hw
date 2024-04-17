from flask import Flask, jsonify, request # handling the import, giving us access to Flask and its functionality
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
# local import for db connection
from connect_db import connect_db, Error
# from marshmallow_sqlalchemy import ModelSchema


app = Flask(__name__)

ma = Marshmallow(app)

# define the member schema
# makes sure the member data adheres to a specific format
class MemberSchema(ma.Schema):
    member_id = fields.Int(dump_only=True)
    name = fields.String()
    email = fields.String()
    phone = fields.String()
    bench_amount = fields.Int()
    membership_type = fields.String()

    class Meta:  
        
        fields = ("member_id", "name", "email", "phone", "bench_amount", "membership_type")

# instantiating MemberSchema class
# based on how many members we're dealing with
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# Dank Sesh Schema
class DankSeshSchema(ma.Schema):
    sesh_id = fields.Int(dump_only=True)
    date = fields.Date()
    member_id = fields.Int()
    workout_type = fields.String()

    class Meta:  
        fields = ("sesh_id", "date", "member_id", "workout_type")

dank_sesh_schema = DankSeshSchema()
dank_seshes_schema = DankSeshSchema(many=True)

@app.route("/") #traffic controller
def home():
    return "Welcome to our super cool fitness tracker, time to get swoll brah!"


@app.route('/members', methods = ['GET'])
def get_members(): 
    print("hello from the get")  
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)
        # SQL query to fetch all customers
        query = "SELECT * FROM Members"

        # executing query with cursor
        cursor.execute(query)

        # accessing stored query
        members = cursor.fetchall()

         # use Marshmallow to format the json response
        return members_schema.jsonify(members)
    
    except Error as e:
        # error handling for connection/route issues
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        #checking again for connection object
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 


# Route to add a member
@app.route('/members', methods = ['POST'])
def add_member():
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        bench_amount = data.get('bench_amount')
        membership_type = data.get('membership_type')

        cursor = conn.cursor()
        query = "INSERT INTO Members (name, email, phone, bench_amount, membership_type) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, phone, bench_amount, membership_type))
        conn.commit()

        return jsonify({"message": "Member added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()



# Route to update a member
@app.route('/members/<int:id>', methods = ['PUT'])
def update_member(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        bench_amount = data.get('bench_amount')
        membership_type = data.get('membership_type')

        cursor = conn.cursor()
        query = "UPDATE Members SET name=%s, email=%s, phone=%s, bench_amount=%s, membership_type=%s WHERE member_id=%s"
        cursor.execute(query, (name, email, phone, bench_amount, membership_type, id))
        conn.commit()

        return jsonify({"message": "Member updated successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Route to delete a member
@app.route('/members/<int:id>', methods = ['DELETE'])
def delete_member(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        query = "DELETE FROM Members WHERE member_id=%s"
        cursor.execute(query, (id,))
        conn.commit()

        return jsonify({"message": "Member deleted successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# Route to retrieve all Dank Seshs
@app.route('/dank-sesh', methods = ['GET'])
def get_dank_sesh():
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Dank_sesh"
        cursor.execute(query)
        seshs = cursor.fetchall()

        return jsonify(seshs)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Route to schedule a Dank Sesh
@app.route('/dank-sesh', methods = ['POST'])
def schedule_dank_sesh():
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        data = request.get_json()
        date = data.get('date')
        member_id = data.get('member_id')
        workout_type = data.get('workout_type')

        cursor = conn.cursor()
        query = "INSERT INTO Dank_sesh (date, member_id, workout_type) VALUES (%s, %s, %s)"
        cursor.execute(query, (date, member_id, workout_type))
        conn.commit()

        return jsonify({"message": "Dank Sesh scheduled successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# Route to update a Dank Sesh
@app.route('/dank-sesh/<int:id>', methods = ['PUT'])
def update_dank_sesh(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        data = request.get_json()
        date = data.get('date')
        member_id = data.get('member_id')
        workout_type = data.get('workout_type')

        cursor = conn.cursor()
        query = "UPDATE Dank_sesh SET date=%s, member_id=%s, workout_type=%s WHERE session_id=%s"
        cursor.execute(query, (date, member_id, workout_type, id))
        conn.commit()

        return jsonify({"message": "Dank Sesh updated successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Route to delete a Dank Sesh
@app.route('/dank-sesh/<int:id>', methods = ['DELETE'])
def delete_dank_sesh(id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        query = "DELETE FROM Dank_sesh WHERE session_id=%s"
        cursor.execute(query, (id,))
        conn.commit()

        return jsonify({"message": "Dank Sesh deleted successfully"}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()





if __name__ == "__main__":
    app.run(debug=True, port=5001)

