
# 🍽️ Elite Catering Services  
### Full Stack Web Application 

A containerized **two-tier full stack web application** built with Flask and MySQL, integrated with DevOps tools for automation and CI/CD.  
This project demonstrates **end-to-end development, containerization, and deployment** using Docker and Jenkins.

---

## 🏗️ Architecture Overview
**Two-Tier Architecture**
- **Frontend:** Static HTML/CSS/JavaScript UI
- **Backend:** Flask REST API with MySQL database
- **DevOps:** Docker, Docker Compose, Jenkins CI/CD

---

## 🚀 Features

### 🎨 Frontend (Tier 1)
- Responsive UI with modern dark theme  
- Pages: Home, Services, Booking, About, Contact  
- Client-side form validation  
- Booking confirmation messages  

### ⚙️ Backend (Tier 2)
- Flask RESTful API  
- MySQL database integration  
- CRUD operations for bookings  
- Admin authentication & booking management  

---

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Database:** MySQL  
- **Containerization:** Docker, Docker Compose  
- **CI/CD:** Jenkins  
- **Version Control:** Git & GitHub  

---

## 📂 Project Structure
```

.
├── backend
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── database_scheme.sql
│   └── .env
│
├── frontend
│   ├── Dockerfile
│   └── index.html
│
├── Jenkinsfile
├── docker-compose.yaml
└── README.md

````

---

## ⚙️ Prerequisites
Ensure the following are installed:
- Docker
- Docker Compose
- Git
- Jenkins (optional, for CI/CD)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Ajay6-six/TWO-TIER-Devops-project.git
cd TWO-TIER-Devops-project
````

### 2️⃣ Configure Environment Variables

Create a `.env` file inside `backend/`:

```env
DB_HOST=database
DB_USER=root
DB_PASSWORD=password
DB_NAME=app_db
```

### 3️⃣ Build & Run Containers

```bash
docker-compose up --build
```

### 4️⃣ Access the Application

* **Frontend:** [http://localhost:3000](http://localhost:3000)
* **Backend API:** [http://localhost:5000](http://localhost:5000)

---

## 🧪 Database

Database schema is available at:

```
backend/database_scheme.sql
```

This initializes required tables during container startup.

---

## 🔁 CI/CD Pipeline (Jenkins)

The Jenkins pipeline automates:

* Source code checkout
* Docker image build
* Container deployment

Pipeline stages:

* Build
* Test
* Deploy

---

## 📌 Future Enhancements

* Add database container (MySQL/PostgreSQL)
* Kubernetes deployment
* Monitoring with Prometheus & Grafana
* Authentication & authorization
* Automated testing

---

## 👨‍💻 Author

**Ajay Krishna**
DevOps & Cloud Enthusiast
