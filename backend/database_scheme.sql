-- Create Database
CREATE DATABASE IF NOT EXISTS catering_db;
USE catering_db;

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- Bookings Table
CREATE TABLE IF NOT EXISTS Bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    service_type ENUM('catering', 'auditorium', 'both') NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    number_of_people INT NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    special_requirements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    INDEX idx_date (date),
    INDEX idx_status (status)
);

-- CateringStaff Table
CREATE TABLE IF NOT EXISTS CateringStaff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    availability ENUM('available', 'busy', 'off') DEFAULT 'available',
    skill_level ENUM('junior', 'senior', 'expert') NOT NULL,
    specialization VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_availability (availability)
);

-- Insert Sample Staff Data
INSERT INTO CateringStaff (name, availability, skill_level, specialization) VALUES
('Chef Marcus Williams', 'available', 'expert', 'French Cuisine'),
('Chef Sofia Rodriguez', 'available', 'expert', 'Italian Cuisine'),
('Chef James Chen', 'available', 'senior', 'Asian Fusion'),
('Server Anna Thompson', 'available', 'senior', 'Fine Dining'),
('Server David Miller', 'available', 'junior', 'Event Service'),
('Bartender Emma Davis', 'available', 'senior', 'Mixology'),
('Coordinator Lisa Anderson', 'available', 'expert', 'Event Planning'),
('Chef Robert Taylor', 'busy', 'expert', 'BBQ & Grilling');

-- Create view for booking summary
CREATE OR REPLACE VIEW booking_summary AS
SELECT 
    b.id,
    b.service_type,
    b.date,
    b.time,
    b.number_of_people,
    b.status,
    u.name as customer_name,
    u.email,
    u.phone
FROM Bookings b
JOIN Users u ON b.user_id = u.id;

-- Sample Queries for Testing
-- SELECT * FROM booking_summary WHERE status = 'pending';
-- SELECT * FROM CateringStaff WHERE availability = 'available';
-- SELECT COUNT(*) as total_bookings, status FROM Bookings GROUP BY status;