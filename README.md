# FitBuddy - AI Fitness Plan Generator

FitBuddy is a web-based application that uses AI to generate personalized workout plans and nutrition tips based on a user's fitness goals.

## Tech Stack
- **Backend:** FastAPI
- **AI:** Google Gemini 1.5 Pro & Flash
- **Database:** SQLite with SQLAlchemy
- **Frontend:** HTML, CSS, Jinja2

## Features
- 7-day personalized workout plan generation
- Nutrition and recovery tips
- Feedback-based plan updating
- Admin dashboard to view all users

## How to Run
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Add your `GOOGLE_API_KEY` in a `.env` file
6. Run the server: `uvicorn app.main:app --reload`