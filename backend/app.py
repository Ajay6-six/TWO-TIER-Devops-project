from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os

# =====================
# STATIC (Frontend)
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))        # backend/
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")       # ../frontend

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)

# =====================
# MYSQL CONFIG (Using Docker ENV)
# =====================
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '123456789'),
    'database': os.getenv('DB_NAME', 'catering_db')
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print("MySQL Error:", e)
        return None

# =====================
# FRONTEND ROUTES
# =====================
@app.route('/')
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# =====================
# DATABASE TABLE SETUP
# =====================
def init_db():
    connection = get_db_connection()
    if not connection:
        print("Database connection failed ❌")
        return

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            service_type ENUM('catering','auditorium','both') NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            number_of_people INT NOT NULL,
            status ENUM('pending','confirmed','cancelled') DEFAULT 'pending',
            special_requirements TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CateringStaff (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            availability ENUM('available','busy','off') DEFAULT 'available',
            skill_level ENUM('junior','senior','expert') NOT NULL,
            specialization VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()
    print("Database initialized ✔")

# =====================
# API: Create Booking
# =====================
@app.route('/api/book', methods=['POST'])
def create_booking():
    data = request.json
    connection = get_db_connection()

    if not connection:
        return jsonify({"success": False, "error": "DB connection failed"}), 500

    try:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO Users (name, email, phone) VALUES (%s, %s, %s)",
            (data['name'], data['email'], data['phone'])
        )
        user_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO Bookings 
            (user_id, service_type, date, time, number_of_people, special_requirements)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            data['service_type'],
            data['date'],
            data['time'],
            data['number_of_people'],
            data.get('special_requirements', '')
        ))

        connection.commit()
        return jsonify({"success": True, "message": "Booking created!", "user_id": user_id}), 201

    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 400

    finally:
        cursor.close()
        connection.close()

# =====================
# API: Get All Bookings
# =====================
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    connection = get_db_connection()

    if not connection:
        return jsonify({"success": False, "error": "DB connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                Bookings.id, Users.name, Users.email, Users.phone,
                Bookings.service_type, Bookings.date, Bookings.time,
                Bookings.number_of_people, Bookings.status, Bookings.created_at
            FROM Bookings
            INNER JOIN Users ON Bookings.user_id = Users.id
            ORDER BY Bookings.created_at DESC
        """)

        bookings = cursor.fetchall()

        for b in bookings:
            b['date'] = str(b['date'])
            b['time'] = str(b['time'])

        return jsonify({"success": True, "bookings": bookings})

    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 400

    finally:
        cursor.close()
        connection.close()

# =====================
# API: Update Booking Status
# =====================
@app.route('/api/update_status', methods=['POST'])
def update_status():
    data = request.json
    booking_id = data.get('id')
    new_status = data.get('status')

    if not booking_id or not new_status:
        return jsonify({"success": False, "error": "Missing fields"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"success": False, "error": "DB connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Bookings 
            SET status = %s 
            WHERE id = %s
        """, (new_status, booking_id))

        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Booking not found"}), 404

        return jsonify({"success": True, "message": "Status updated"})

    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# =====================
# API: Get Staff
# =====================
@app.route('/api/staff', methods=['GET'])
def get_staff():
    connection = get_db_connection()

    if not connection:
        return jsonify({"success": False, "error": "DB connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CateringStaff")
        staff = cursor.fetchall()
        return jsonify({"success": True, "staff": staff})

    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# =====================
# API: Delete Booking
# =====================
@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    connection = get_db_connection()

    if not connection:
        return jsonify({"success": False, "error": "DB connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Bookings WHERE id = %s", (booking_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Not found"}), 404

        return jsonify({"success": True, "message": "Deleted"})

    except Error as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# =====================
# API: Contact Form
# =====================
@app.route('/api/contact', methods=['POST'])
def contact():
    print("Contact Message:", request.json)
    return jsonify({"success": True, "message": "Message received!"})

# =====================
# API: Admin Login
# =====================
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == 'admin123':
        return jsonify({"success": True, "token": "admin-token"})
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

# =====================
# RUN SERVER
# =====================
if __name__ == "__main__":
    # Initialize database before starting server
    init_db()
    app.run(host="0.0.0.0", debug=True, port=5000)
