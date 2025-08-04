import os
import csv
import sqlite3
from core import DATABASE_FOLDER


def save_to_csv(tenders, filename):
    os.makedirs(DATABASE_FOLDER, exist_ok=True)
    full_path = os.path.join(DATABASE_FOLDER, filename)

    keys = ["number", "link", "customer", "products", "deadline", "publish_date"]
    with open(full_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(tenders)
        print(f"Сохранено {len(tenders)} тендеров в базу данных {full_path}")


def save_to_sqlite(tenders, db_file):
    os.makedirs(DATABASE_FOLDER, exist_ok=True)
    full_path = os.path.join(DATABASE_FOLDER, db_file)

    conn = sqlite3.connect(full_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tenders (
        number TEXT,
        link TEXT,
        customer TEXT,
        products TEXT,
        deadline TEXT,
        publish_date TEXT
    )
    """)

    cursor.execute("DELETE FROM tenders")

    for tender in tenders:
        cursor.execute("""
            INSERT INTO tenders (number, link, customer, products, deadline, publish_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            tender["number"],
            tender["link"],
            tender["customer"],
            tender["products"],
            tender["deadline"],
            tender["publish_date"]
        ))

    conn.commit()
    conn.close()
    print(f"Сохранено {len(tenders)} тендеров в базу данных {full_path}")
