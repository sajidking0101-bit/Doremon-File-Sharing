"""
Database Module - Handle file and user data persistence
"""

import sqlite3
import json
from typing import List, Dict, Optional
from datetime import datetime

DATABASE_FILE = 'bot.db'


class Database:
    """SQLite database handler for bot data."""
    
    def __init__(self, db_file: str = DATABASE_FILE):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self) -> None:
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                file_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                locked BOOLEAN DEFAULT 1,
                unlock_cost INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User unlocks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_unlocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                file_id TEXT NOT NULL,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (file_id) REFERENCES files(file_id),
                UNIQUE(user_id, file_id)
            )
        ''')
        
        # Download history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS download_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                file_id TEXT NOT NULL,
                downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (file_id) REFERENCES files(file_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None) -> None:
        """Add or update user."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
        ''', (user_id, username, first_name))
        
        conn.commit()
        conn.close()
    
    def add_file(self, file_id: str, name: str, path: str, 
                 locked: bool = True, unlock_cost: int = 0) -> None:
        """Add a new file to database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO files (file_id, name, path, locked, unlock_cost)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_id, name, path, locked, unlock_cost))
        
        conn.commit()
        conn.close()
    
    def get_all_files(self) -> List[Dict]:
        """Get all files."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM files')
        files = []
        for row in cursor.fetchall():
            files.append({
                'file_id': row[0],
                'name': row[1],
                'path': row[2],
                'locked': bool(row[3]),
                'unlock_cost': row[4]
            })
        
        conn.close()
        return files
    
    def unlock_file(self, user_id: int, file_id: str) -> bool:
        """Unlock a file for a user."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_unlocks (user_id, file_id)
                VALUES (?, ?)
            ''', (user_id, file_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Already unlocked
            return False
        finally:
            conn.close()
    
    def is_file_unlocked(self, user_id: int, file_id: str) -> bool:
        """Check if a file is unlocked for a user."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 1 FROM user_unlocks
            WHERE user_id = ? AND file_id = ?
        ''', (user_id, file_id))
        
        result = cursor.fetchone() is not None
        conn.close()
        return result
    
    def get_user_unlocks(self, user_id: int) -> List[str]:
        """Get all unlocked files for a user."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT file_id FROM user_unlocks
            WHERE user_id = ?
        ''', (user_id,))
        
        file_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return file_ids
    
    def log_download(self, user_id: int, file_id: str) -> None:
        """Log file download."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO download_history (user_id, file_id)
            VALUES (?, ?)
        ''', (user_id, file_id))
        
        conn.commit()
        conn.close()
    
    def get_download_stats(self, file_id: str) -> int:
        """Get download count for a file."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM download_history
            WHERE file_id = ?
        ''', (file_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count


# Global database instance
db = Database()
