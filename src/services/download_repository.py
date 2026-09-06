from pathlib import Path
import sqlite3

class DownloadRepository():
    def __init__(self, database):
        self.database = Path(database)

    def initialize(self):
        with sqlite3.connect(self.database) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS downloads (
                    id TEXT PRIMARY KEY,
                    url TEXT NOT NULL,
                    status TEXT NOT NULL,
                    filename TEXT,
                    path TEXT,
                    error TEXT,
                    created_at TEXT,
                    completed_at TEXT
                )
            """)

            conn.commit()

    def create(self, download_id: str, url: str):
        with sqlite3.connect(self.database) as conn:
            conn.execute("""
                INSERT INTO downloads (
                    id,
                    url,
                    status
                )
                VALUES (?, ?, ?)
            """, (
                download_id,
                url,
                "pending"
            ))

            conn.commit()

            return download_id

    def get(self, download_id: str):
        with sqlite3.connect(self.database) as conn:
            conn.row_factory = sqlite3.Row

            row = conn.execute("""
                SELECT *
                FROM downloads
                WHERE id = ?
            """, (download_id,)).fetchone()

            return dict(row) if row else None

    def update_status(self, download_id: str, status: str):
        with sqlite3.connect(self.database) as conn:
            conn.execute("""
                UPDATE downloads
                SET status = ?
                WHERE id = ?
            """, (status, download_id))

            conn.commit()

    def complete(
        self,
        download_id: str,
        filename: str,
        path: str,
        #completed_at: str
    ):
        with sqlite3.connect(self.database) as conn:
            conn.execute("""
                UPDATE downloads
                SET
                    status = ?,
                    filename = ?,
                    path = ?
                WHERE id = ?
            """, (
                "complete",
                filename,
                path,
                #completed_at,
                download_id
            ))

            conn.commit()

    def fail(self, download_id: str, error: str):
        with sqlite3.connect(self.database) as conn:
            conn.execute("""
                UPDATE downloads
                SET
                    status = ?,
                    error = ?
                WHERE id = ?
            """, (
                "failed",
                error,
                download_id
            ))

            conn.commit()
    
    