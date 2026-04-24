# Medhavi University Fee Tracker

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Status](https://img.shields.io/badge/Status-Active-success)

A full-stack web application to manage and track student fee payments with CSV upload, filtering, and export functionality.

---

## Features

- Upload CSV for bulk fee updates  
- Track Paid / Unpaid students  
- Filter by Month, Year, Batch, Status  
- Export data as CSV  
- Real-time refresh after upload  
- Clean UI with status highlighting  

---

## Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Flask (Python) |
| Database | PostgreSQL |
| Libraries | Pandas, psycopg2, Flask-CORS |

---

## Project Structure
ASSIGNMENT/
│── backend/
│ │── app.py
│ │── db.py
│ │── routes/
│ │ └── fees.py
│
│── database/
│ └── schema.sql
│
│── frontend/
│ │── index.html
│ │── script.js
│ │── style.css
│ 
│── sample_data.csv
│── README.md
## Installation & Setup

### 1. Clone Repository


git clone https://github.com/your-username/fee-tracker.git

cd fee-tracker


---

### 2. Backend Setup


cd backend
python -m venv venv
venv\Scripts\activate # Windows
pip install flask pandas psycopg2 flask-cors


---

### 3. Database Setup

Run the SQL file:


database/schema.sql


---

### 4. Configure Database

Update credentials in:


backend/db.py

password="your_password"


---

### 5. Run Backend Server


python app.py


Server runs at:


http://127.0.0.1:5000


---

### 6. Run Frontend

Open:


frontend/index.html


---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|------------|
| GET | `/fees?month=3&year=2026` | Get fee status |
| POST | `/upload-csv` | Upload CSV |
| GET | `/export?month=3&year=2026` | Export CSV |

---

## CSV Format

Required columns:


roll_number,month,year,amount_paid,payment_date


### Example:


ME001,3,2026,50000,2026-03-05
CSE001,3,2026,50000,2026-03-06


---

## Frontend Highlights

- Auto-fetch data on load  
- Dynamic filters (Batch, Status)  
- CSV upload with instant feedback  
- Highlight unpaid students in red  
- One-click export  

---

## Error Handling

- Missing columns → Error  
- Invalid dates → Rejected  
- Unknown roll numbers → Skipped  
- DB errors → Rollback  

---

## Backend Highlights

- LEFT JOIN → detect unpaid students  
- ON CONFLICT → update existing records  
- Handles encoding issues (`utf-8`, `latin1`)  
- Cleans CSV columns automatically  

---

## Future Improvements

- Authentication system  
- Dashboard with charts  
- Deployment (AWS / Render)  
- Mobile responsive UI  

---

## Author

**Shubhjeet Paul**  
Data Analyst | Python Developer | ML Enthusiast  

---

## Support

If you like this project:

- Star this repo  
- Fork it  
- Contribute  