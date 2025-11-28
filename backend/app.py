from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__, static_folder='static')
CORS(app)

# ============================
# MySQL Database Configuration
# ============================

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',   
    'database': 'catering_db'
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print("MySQL Connection Error:", e)
        return None

# ============================
# Database Initialization
# ============================

def init_db():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                service_type ENUM('catering', 'auditorium', 'both') NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                number_of_people INT NOT NULL,
                status ENUM('pending','confirmed','cancelled') DEFAULT 'pending',
                special_requirements TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CateringStaff (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                availability ENUM('available','busy','off') DEFAULT 'available',
                skill_level ENUM('junior','senior','expert') NOT NULL,
                specialization VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized ✔")

# ============================
# FRONTEND ROUTES
# ============================

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_page(path):
    return send_from_directory('static', path)

# ============================
# API ROUTES
# ============================

# Create Booking
@app.route('/api/book', methods=['POST'])
def create_booking():
    try:
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Users (name, email, phone) VALUES (%s, %s, %s)",
                       (data['name'], data['email'], data['phone']))
        user_id = cursor.lastrowid

        cursor.execute('''INSERT INTO Bookings 
            (user_id, service_type, date, time, number_of_people, special_requirements)
            VALUES (%s, %s, %s, %s, %s, %s)''',
            (user_id, data['service_type'], data['date'], data['time'],
             data['number_of_people'], data.get('special_requirements', '')))

        connection.commit()
        return jsonify({"success": True, "message": "Booking created!", "user_id": user_id}), 201

    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

# ============================
# 📌 Get All Bookings
# ============================

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                Bookings.id,
                Users.name,
                Users.email,
                Users.phone,
                Bookings.service_type,
                Bookings.date,
                Bookings.time,
                Bookings.number_of_people,
                Bookings.status,
                Bookings.created_at
            FROM Bookings
            INNER JOIN Users ON Bookings.user_id = Users.id
            ORDER BY Bookings.created_at DESC
        """)

        bookings = cursor.fetchall()

        # Convert date + time to string
        for b in bookings:
            b['date'] = str(b['date'])
            b['time'] = str(b['time'])

        return jsonify({"success": True, "bookings": bookings}), 200

    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 400

    finally:
        cursor.close()
        connection.close()



# ============================
# ⭐ Update Booking Status (POST)
# ============================

@app.route('/api/update_status', methods=['POST'])
def update_status():
    try:
        data = request.json
        booking_id = data.get('id')
        new_status = data.get('status')

        # Validation
        if not booking_id:
            return jsonify({"success": False, "error": "Booking ID is required"}), 400

        if not new_status:
            return jsonify({"success": False, "error": "New status is required"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Bookings 
            SET status = %s 
            WHERE id = %s
        """, (new_status, booking_id))

        connection.commit()

        # If no rows were updated
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Booking not found"}), 404

        return jsonify({"success": True, "message": "Status updated successfully"}), 200

    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()


# ============================
# Staff API
# ============================

@app.route('/api/staff', methods=['GET'])
def get_staff():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CateringStaff")
        staff = cursor.fetchall()
        return jsonify({"success": True, "staff": staff}), 200
    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        cursor.close()
        connection.close()

@app.route('/api/bookings/<int:booking_id>', methods=['PUT'])
def update_booking_status(booking_id):
    try:
        data = request.json
        new_status = data.get('status')

        if not new_status:
            return jsonify({"success": False, "error": "Status is required"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Bookings 
            SET status = %s 
            WHERE id = %s
        """, (new_status, booking_id))
        
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Booking not found"}), 404

        return jsonify({"success": True, "message": "Status updated successfully"}), 200

    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Bookings WHERE id = %s", (booking_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Booking not found"}), 404

        return jsonify({"success": True, "message": "Booking deleted successfully"}), 200

    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()


# Contact API
@app.route('/api/contact', methods=['POST'])
def contact():
    print("Contact Message:", request.json)
    return jsonify({"success": True, "message": "Message received!"}), 200

# Admin Login
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == 'admin123':
        return jsonify({"success": True, "token": "admin-token"}), 200
    return jsonify({"success": False, "error": "Invalid credentials"}), 401


# ============================
# RUN APP
# ============================

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
