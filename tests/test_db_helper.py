import csv
import sqlite3

from database.db_helper import save_to_sqlite, save_to_csv

example_tenders = [
    {
        "number": "123",
        "link": "http://example.com/1",
        "customer": "Компания А",
        "products": "Товар 1",
        "deadline": "2025-08-15",
        "publish_date": "2025-08-01"
    },
    {
        "number": "456",
        "link": "http://example.com/2",
        "customer": "Компания Б",
        "products": "Товар 2",
        "deadline": "2025-09-01",
        "publish_date": "2025-08-05"
    }
]

def test_save_to_csv_creates_file_and_content(tmp_path):
    csv_file = tmp_path / "test_tenders.csv"
    save_to_csv(example_tenders, str(csv_file))
    assert csv_file.exists()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == len(example_tenders)
    assert rows[0]['number'] == example_tenders[0]['number']
    assert rows[1]['customer'] == example_tenders[1]['customer']


def test_save_to_sqlite_creates_db_and_table(tmp_path):
    db_file = tmp_path / "test_tenders.db"
    save_to_sqlite(example_tenders, str(db_file))
    assert db_file.exists()

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tenders'")
    table_exists = cursor.fetchone()
    assert table_exists is not None

    cursor.execute("SELECT COUNT(*) FROM tenders")
    count = cursor.fetchone()[0]
    assert count == len(example_tenders)

    cursor.execute("SELECT number, customer FROM tenders ORDER BY number")
    rows = cursor.fetchall()
    assert rows[0][0] == example_tenders[0]["number"]
    assert rows[1][1] == example_tenders[1]["customer"]
    conn.close()
