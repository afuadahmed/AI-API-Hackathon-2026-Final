# Civic AI – AI-Powered Civic Issue Reporting Platform

An AI-powered civic issue reporting platform built for the **AI & API Hackathon 2026**.

Citizens can report incidents, while AI automatically analyzes severity, assigns the responsible department, detects duplicate reports, and provides a public tracking system with progress updates.

---

## Features

### Citizen Portal
- Submit civic incident reports
- Upload supporting images
- Automatic tracking code generation
- Public report tracking

### AI Analysis
- Google Gemini AI integration
- Priority classification
- Severity score (0–100)
- AI confidence score
- Responsible department assignment
- AI-generated incident summary
- AI reasoning

### Duplicate Detection
- Detects similar reports
- Links duplicate incidents
- Synchronizes status across linked reports

### Government Dashboard
- View all submitted reports
- Search reports
- Filter by:
  - Status
  - Category
  - Priority
- Update incident status
- Dashboard statistics
- Duplicate indicators

### Progress Tracking
- Submission history
- AI analysis history
- Department assignment history
- Status update history

---

## Technologies Used

- Python
- Django
- Bootstrap 5
- Google Gemini API
- SQLite (Development & Demo)
- Render (Deployment)

---

## AI Workflow

Citizen Report

↓

Gemini AI Analysis

↓

Priority Classification

↓

Severity Scoring

↓

Department Assignment

↓

Duplicate Detection

↓

Government Dashboard

↓

Public Tracking

---

## Project Structure

```
civic_ai/
│
├── civic_ai/
├── reports/
│   ├── models.py
│   ├── views.py
│   ├── services/
│   │   ├── ai_service.py
│   │   └── duplicate_service.py
│   ├── forms.py
│   └── urls.py
│
├── templates/
├── static/
├── media/
├── requirements.txt
└── manage.py
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/afuadahmed/AI-API-Hackathon-2026-Final.git
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=your_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True
```

Run migrations

```bash
python manage.py migrate
```

Start the server

```bash
python manage.py runserver
```

---

## Live Demo

https://ai-api-hackathon-2026-final.onrender.com

---

## Repository

https://github.com/afuadahmed/AI-API-Hackathon-2026-Final

---

## Future Improvements

- Bengali language support
- PostgreSQL production database
- Interactive GIS map integration
- Email/SMS notifications
- Citizen authentication
- Government analytics dashboard
- Mobile application

---

## Team

**Fuad Ahmed**

AI & API Hackathon 2026

---

## License

This project was developed for educational and hackathon purposes.
