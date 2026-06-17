# import os
# import psycopg2
# from dotenv import load_dotenv

# load_dotenv()

# conn = psycopg2.connect(
# host=os.getenv("DB_HOST"),
# port=os.getenv("DB_PORT"),
# dbname=os.getenv("DB_NAME"),
# user=os.getenv("DB_USER"),
# password=os.getenv("DB_PASSWORD")
# )

# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS expenses (
# id SERIAL PRIMARY KEY,
# expense_date DATE NOT NULL,
# amount NUMERIC(10,2) NOT NULL,
# category VARCHAR(100) NOT NULL,
# subcategory VARCHAR(100),
# note TEXT,
# created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# """)

# conn.commit()

# cursor.close()
# conn.close()

# print("Expense table created successfully.")


import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    sslmode="require"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    expense_date DATE NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()

cur.close()
conn.close()

print("Database initialized successfully.")