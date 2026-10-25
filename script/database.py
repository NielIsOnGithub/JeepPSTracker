import sqlite3

class GPSDatabase:
    def __init__(self, db_name) -> None:
        self.database_name = db_name

        self.connection = sqlite3.connect(db_name + ".db")
        self.connection.row_factory = sqlite3.Row

        cursor = self.connection.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database_name} (
                id TEXT PRIMARY KEY,
                type TEXT,
                latitude REAL,
                longitude REAL,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    
        self.connection.commit() 
    
        print("Database initialized successfully.")

    def update(self, device_id: str, device_type: str, latitude: float, longitude: float) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            f"""
            INSERT OR REPLACE INTO {self.database_name} (id, type, latitude, longitude, last_updated) 
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (device_id, device_type, latitude, longitude)
        )

        self.connection.commit()

    def get(self, device_id: str) -> sqlite3.Row | None:
        cursor = self.connection.cursor()
        cursor.execute(
            f"""SELECT latitude, longitude FROM {self.database_name} WHERE id = ?""",
            (device_id,)
        )

        return cursor.fetchone()

    def close(self):
        self.connection.close()

        print("Database connection closed.")