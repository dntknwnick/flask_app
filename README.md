# Jishu Backend API

This is the backend API for the Jishu exam preparation application, built with Flask and MySQL.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- MySQL server
- pip (Python package manager)

### Installation

1. Create a MySQL database:
```sql
CREATE DATABASE jishu_db;
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python init_db.py
```

4. Run the application:
```bash
python run.py
```

The API will be available at http://localhost:5000

## API Endpoints

### Authentication
- `POST /auth/request-otp` - Request an OTP for login
- `POST /auth/verify-otp` - Verify OTP and get access token
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user details

### Exam Categories
- `GET /api/exam-categories` - Get all exam categories
- `GET /api/exam-categories/<id>` - Get a specific exam category
- `POST /api/exam-categories` - Create a new exam category (admin only)
- `PUT /api/exam-categories/<id>` - Update an exam category (admin only)
- `DELETE /api/exam-categories/<id>` - Delete an exam category (admin only)

### Subjects
- `GET /api/subjects` - Get all subjects (can filter by category_id)
- `GET /api/subjects/<id>` - Get a specific subject
- `POST /api/subjects` - Create a new subject (admin only)
- `PUT /api/subjects/<id>` - Update a subject (admin only)
- `DELETE /api/subjects/<id>` - Delete a subject (admin only)

### Questions
- `GET /api/questions` - Get all questions (can filter by subject_id)
- `GET /api/questions/<id>` - Get a specific question
- `POST /api/questions` - Create a new question with options (admin only)
- `PUT /api/questions/<id>` - Update a question (admin only)
- `DELETE /api/questions/<id>` - Delete a question (admin only)

### User Progress
- `GET /api/user/exams` - Get all exams purchased by the current user
- `POST /api/user/exams/<subject_id>/purchase` - Purchase an exam (can purchase multiple times)
- `POST /api/user/exams/<user_exam_id>/start` - Start a new exam attempt
- `POST /api/user/attempts/<attempt_id>/submit` - Submit an exam attempt with answers
- `GET /api/user/attempts` - Get all exam attempts by the current user
- `GET /api/user/attempts/<attempt_id>` - Get details of a specific exam attempt

## Demo Users

For testing purposes, the following users are created by default:

- Admin: Mobile number `9876543210`
- Student: Mobile number `9876543211`

When requesting an OTP, the OTP will be printed to the console (in a production environment, it would be sent via SMS).

## Sample Data

The initialization script creates sample data including:

- Exam categories (NEET, JEE Advanced, JEE Mains, CET)
- Subjects for each category
- Sample questions for NEET Physics and Chemistry
- A sample user (Student) who has purchased the NEET Physics subject 3 times
- Two exam attempts for the student with different scores

## Exam Purchase and Retake System

This backend implements a purchase and retake system for exams:

1. **Limited Retakes Per Purchase**:
   - Users can purchase a subject test (e.g., Physics) once
   - Each purchase comes with a limited number of retakes (default: 3)
   - After using all retakes, users must purchase the exam again to get more attempts

2. **Purchase Tracking**:
   - The system tracks purchase count and purchase dates
   - When a user purchases an exam again, their retake count is reset

3. **Attempt Tracking**:
   - Each attempt is numbered sequentially
   - All attempt history and scores are preserved in the database
   - The system tracks how many retakes have been used and how many remain

This system allows students to practice subjects with a limited number of attempts per purchase, encouraging them to purchase again after using all their retakes.
