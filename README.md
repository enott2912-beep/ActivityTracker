# Activity Tracker Bot

A Telegram bot for tracking daily tasks, analyzing productivity (using AI), and maintaining a streak.

## Features

*   **Daily Tasks**: Manage today's to-do list with interactive buttons.
*   **Statistics**: View progress, completion rates, and streak counters.
*   **AI Analysis**: Get productivity insights via DeepSeek, Ollama, or OpenAI.
*   **Reminders**: Automatic notifications 1 hour before a scheduled task using a background scheduler.
*   **Categories**: Organize tasks by Sport, Study, or Other.
*   **Asynchronous Database**: Non-blocking database operations for high performance.

## Tech Stack

*   **Language**: Python 3.10+
*   **Bot Framework**: `aiogram 3.x`
*   **Database**: SQLite + `aiosqlite` (Async)
*   **Scheduling**: `APScheduler`
*   **AI Integration**: `openai` (Python library compatible with DeepSeek/Ollama)
*   **Configuration**: `python-dotenv`

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/activity-tracker.git
    cd activity-tracker
    ```

2.  Install dependencies:
    ```bash
    pip install aiogram aiosqlite apscheduler openai python-dotenv
    ```

3.  Create a `.env` file in the root directory:
    ```env
    BOT_TOKEN=your_telegram_bot_token
    
    # Optional: Select AI Mode (ollama, deepseek, openai). Default: ollama
    AI_MODE=ollama
    
    # If using DeepSeek
    DEEPSEEK_API_KEY=your_key
    
    # If using OpenAI (or compatible API)
    OPENAI_API_KEY=your_key
    ```

## Usage

Run the bot with:

```bash
python app.py
```

**Commands:**
*   `/start` - Open main menu.
*   `/add` - Add a new task interactively.
*   `/today` - Show today's tasks.
*   `/stats` - Show productivity stats and current streak.
*   `/analyze` - Request an AI summary of your progress.

## Project Structure

*   `app.py`: Main entry point.
*   `config.py`: Configuration and environment variables.
*   `handlers/`: Telegram message handlers (Business logic layer).
*   `services/`: Core logic and Database interactions (Data layer).
*   `db/`: Database setup and file storage.
*   `utils/`: Helper functions (display, formatting).

## Future Improvements

*   [ ] Add Docker support (`Dockerfile` & `docker-compose`).
*   [ ] Migrate to PostgreSQL for better scalability.
*   [ ] Add User Timezone support for accurate notifications.
*   [ ] Implement recurring tasks (daily, weekly).
    ```bash
    python app.py
    ```

## AI Configuration

The bot supports three AI backends defined in `services/ai_service.py`:

1.  **Ollama (Local)**: Runs locally on port 11434. Default model: `phi3:mini`.
2.  **DeepSeek**: Requires API key.
3.  **OpenAI**: Requires API key.

If the AI service is unavailable, the bot falls back to a simple algorithmic analysis.

## Database

The bot uses SQLite (`db/activitytracker.db`). The database is initialized automatically on the first run.
