# ActivityTracker

## Description
ActivityTracker is a Telegram bot that helps users manage and track their daily activities related to **study and sport**.

The bot allows users to:
- plan learning sessions and workouts
- track completed activities
- monitor progress over time
- receive simple recommendations based on activity statistics

This project was created as a **final project for CS50**.

---

## Features (MVP)
- Add study or sport activities
- View daily plan
- Mark activities as completed
- Track progress and streaks
- Simple analytics and recommendations

---

## Tech Stack
- Python 3.10+
- aiogram 3.x
- SQLite
- Git & GitHub

---

## Project Structure
ActivityTracker/
- ├── app.py
- ├── config.py
- ├── handlers/
- ├── services/
- ├── db/
- ├── utils/
- ├── .env.example
- ├── .gitignore
- └── README.md

---

## How to Run
1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies
4. Create `.env` file with your Telegram Bot Token
5. Run `python app.py`

---

## Notes
The project focuses on clean architecture, async programming, and practical data analysis rather than complex machine learning models.
