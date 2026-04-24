--create Database
Create Database db_student;

-- Connect to DB (works in psql)
\c db_student;

-- Students Table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    batch_name VARCHAR(100) NOT NULL
);


-- Fees Table
CREATE TABLE fees (
    fee_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id) ON DELETE CASCADE,
    month INT NOT NULL,
    year INT NOT NULL,
    amount_paid NUMERIC(10,2),
    payment_date DATE,
    UNIQUE(student_id, month, year)
);

-- Index
CREATE INDEX idx_fee_lookup 
ON fees(student_id, month, year);

-- Sample Data
INSERT INTO students (name, roll_number, batch_name) VALUES
('Aman Sharma', 'ME001', '2025 - Aug - B.Tech ME'),
('Riya Singh', 'CSE001', '2025 - Aug - B.Tech CSE'),
('Rahul Verma', 'CE001', '2025 - Aug - B.Tech CE'),
('Neha Gupta', 'CSE002', '2025 - Aug - B.Tech CSE'),
('Karan Patel', 'ME002', '2025 - Aug - B.Tech ME');

INSERT INTO fees (student_id, month, year, amount_paid, payment_date) VALUES
(1, 3, 2026, 50000, '2026-03-05'),
(2, 3, 2026, 50000, '2026-03-06'),
(4, 3, 2026, 50000, '2026-03-07');