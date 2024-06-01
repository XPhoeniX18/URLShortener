import sqlite3

conn = sqlite3.connect('urls.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_url TEXT NOT NULL UNIQUE
)
''')
conn.commit()
conn.close()