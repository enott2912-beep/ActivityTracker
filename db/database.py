import aiosqlite
import asyncio
import os
from config import DB_PATH

async def setup_database():
    """
    Initializes the database: creates directory, DB file, and 'tasks' table if not exists.
    """
    base_dir = os.path.dirname(DB_PATH)
    os.makedirs(base_dir, exist_ok=True)

    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            await conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_done BOOLEAN DEFAULT FALSE,
                category TEXT,
                date DATE,
                time TIME,
                reminder_job_id TEXT,
                done_at TIMESTAMP        
            )''')
            await conn.commit()
            print(f"Database '{DB_PATH}' and table 'tasks' verified/created.")
    except Exception as e:
        print(f"DB Error: {e}")

if __name__ == "__main__":
    asyncio.run(setup_database())