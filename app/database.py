import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class ConversationDB:
    
    def __init__(self, db_path: str = "conversations.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    model TEXT NOT NULL,
                    prompt_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tokens_used INTEGER DEFAULT 0,
                    cost REAL DEFAULT 0.0,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_conversation_updated 
                ON conversations(updated_at DESC)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_conversation 
                ON messages(conversation_id, timestamp)
            """)
    
    def create_conversation(self, title: str, model: str, prompt_id: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversations (title, model, prompt_id)
                VALUES (?, ?, ?)
            """, (title, model, prompt_id))
            return cursor.lastrowid
    
    def add_message(self, conversation_id: int, role: str, content: str, 
                   tokens_used: int = 0, cost: float = 0.0) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO messages (conversation_id, role, content, tokens_used, cost)
                VALUES (?, ?, ?, ?, ?)
            """, (conversation_id, role, content, tokens_used, cost))
            
            cursor.execute("""
                UPDATE conversations 
                SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (conversation_id,))
            
            return cursor.lastrowid
    
    def get_conversation_messages(self, conversation_id: int) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT role, content, timestamp, tokens_used, cost
                FROM messages 
                WHERE conversation_id = ?
                ORDER BY timestamp ASC
            """, (conversation_id,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def list_conversations(self, limit: int = 20) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.id, c.title, c.model, c.prompt_id, c.created_at, c.updated_at,
                       COUNT(m.id) as message_count,
                       ROUND(SUM(m.cost), 6) as total_cost
                FROM conversations c
                LEFT JOIN messages m ON c.id = m.conversation_id
                GROUP BY c.id
                ORDER BY c.updated_at DESC
                LIMIT ?
            """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def search_conversations(self, query: str, limit: int = 10) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT c.id, c.title, c.model, c.created_at,
                       COUNT(m.id) as message_count
                FROM conversations c
                JOIN messages m ON c.id = m.conversation_id
                WHERE m.content LIKE ? OR c.title LIKE ?
                GROUP BY c.id
                ORDER BY c.updated_at DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_conversation(self, conversation_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            
            cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            
            return cursor.rowcount > 0
    
    def get_conversation_info(self, conversation_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT c.*, COUNT(m.id) as message_count, 
                       ROUND(SUM(m.cost), 6) as total_cost
                FROM conversations c
                LEFT JOIN messages m ON c.id = m.conversation_id
                WHERE c.id = ?
                GROUP BY c.id
            """, (conversation_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_conversation_title(self, conversation_id: int, new_title: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE conversations 
                SET title = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_title, conversation_id))
            return cursor.rowcount > 0
    
    def get_stats(self) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT c.id) as total_conversations,
                    COUNT(m.id) as total_messages,
                    ROUND(SUM(m.cost), 6) as total_cost,
                    COUNT(DISTINCT c.model) as models_used,
                    COUNT(DISTINCT c.prompt_id) as prompts_used
                FROM conversations c
                LEFT JOIN messages m ON c.id = m.conversation_id
            """)
            
            return dict(cursor.fetchone())
    
    def clean_duplicate_system_messages(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT conversation_id, COUNT(*) as system_count
                FROM messages 
                WHERE role = 'system'
                GROUP BY conversation_id
                HAVING COUNT(*) > 1
            """)
            
            affected_conversations = cursor.fetchall()
            total_deleted = 0
            
            for conv_id, count in affected_conversations:
                cursor.execute("""
                    DELETE FROM messages 
                    WHERE conversation_id = ? AND role = 'system' 
                    AND id NOT IN (
                        SELECT id FROM messages 
                        WHERE conversation_id = ? AND role = 'system'
                        ORDER BY timestamp DESC 
                        LIMIT 1
                    )
                """, (conv_id, conv_id))
                
                deleted = cursor.rowcount
                total_deleted += deleted
                
            return total_deleted

conversation_db = ConversationDB()
