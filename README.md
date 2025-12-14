
# 🍽️ Elite Catering Services – Full Stack Web Application

A brief description of what this project does and who it's for

🍽️ Elite Catering Services – Full Stack Web Application (DevOps Enabled)

Elite Catering Services is a 2-tier full stack web application built using Flask and MySQL, enhanced with DevOps tools for containerization, automation, and CI/CD. The project demonstrates end-to-end application development and deployment practices.

🏗️ Project Structure
.
├── backend
│   ├── __pycache__/              # Python cache files
│   ├── .env                      # Backend environment variables
│   ├── Dockerfile                # Backend Docker image configuration
│   ├── app.py                    # Flask backend application
│   ├── database_scheme.sql       # MySQL database schema
│   └── requirements.txt          # Python dependencies
│
├── frontend
│   ├── Dockerfile                # Frontend Docker image configuration
│   └── index.html                # Frontend user interface
│
├── Jenkinsfile                   # Jenkins CI/CD pipeline definition
├── docker-compose.yaml           # Multi-container Docker orchestration
└── README.md              

🚀 Features
🎨 Frontend (Tier 1)

✅ Responsive HTML, CSS, and JavaScript UI with modern dark theme

✅ Five core pages: Home, Services, Book, About, Contact

✅ Mobile-friendly navigation menu

✅ Client-side form validation and error handling

✅ Booking confirmation messages

✅ Admin dashboard for booking management

⚙️ Backend (Tier 2)

✅ Flask RESTful backend using Python

✅ MySQL database integration

✅ CRUD operations for bookings

✅ User and admin management system

✅ Staff availability tracking

✅ Secure admin authentication

🛠️ Tech Stack

Backend: Python (Flask)

Frontend: HTML

Database: SQL (schema provided)

Containerization: Docker & Docker Compose

CI/CD: Jenkins

Version Control: Git

⚙️ Prerequisites

Make sure you have the following installed:

Docker

Docker Compose

Git

Jenkins (for CI/CD pipeline)

🚀 Getting Started
1️⃣ Clone the Repository
git clone https://github.com/Ajay6-six/TWO-TIER-Devops-project.git
cd TWO-TIER-Devops-project

2️⃣ Environment Variables

Create a .env file inside the backend directory:

DB_HOST=database
DB_USER=root
DB_PASSWORD=password
DB_NAME=app_db

3️⃣ Build and Run Using Docker Compose
docker-compose up --build

4️⃣ Access the Application

Frontend: http://localhost:3000

Backend API: http://localhost:5000

(Ports may vary based on docker-compose.yaml)

🧪 Database Setup

The database schema is available at:

backend/database_scheme.sql


This file initializes the required database tables when the container starts.

🔁 CI/CD Pipeline (Jenkins)

The Jenkinsfile automates:

Source code checkout

Docker image build

Container deployment

Sample Jenkins Pipeline Stages:

Build

Test

Deploy

📦 Docker Details
Backend

Uses Python base image

Installs dependencies from requirements.txt

Runs app.py

Frontend

Uses lightweight web server

Serves static HTML content

📄 docker-compose.yaml

The docker-compose.yaml file:

Defines backend & frontend services

Manages networking between containers

Enables single-command deployment

📌 Future Improvements

Add database container (MySQL/PostgreSQL)

Implement authentication

Add unit and integration tests

Kubernetes deployment

Monitoring with Prometheus & Grafana

👨‍💻 Author

Ajay Krishna
DevOps & Cloud Enthusiast
