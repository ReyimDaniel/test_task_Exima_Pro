from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import argparse
from database import save_to_sqlite, save_to_csv
from core import BASE_URL


def parse_b2b_center_selenium(url, max_items=100):
    options = Options()
    options.add_argument("--headless=new")  # ← новый стабильный headless режим
    options.add_argument("--disable-gpu")  # ← полезен для Windows
    options.add_argument("--no-sandbox")  # ← для Linux/CI
    options.add_argument("--window-size=1920,1080")  # ← нужно, если элементы исчезают в headless
    options.headless = True
    driver = webdriver.Chrome(options=options)
    tenders = []
    try:
        page = 1
        while len(tenders) < max_items:
            driver.get(url)
            wait = WebDriverWait(driver, 15)
            wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "table.table tbody tr")))
            table = driver.find_element(By.CSS_SELECTOR, "table.table tbody")
            rows = table.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                if len(tenders) >= max_items:
                    break
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) < 5:
                    continue

                link_elem = cols[0].find_element(By.TAG_NAME, "a")
                tender_number = link_elem.text.strip().split('\n')[0]
                tender_link = link_elem.get_attribute("href")

                try:
                    desc_elem = cols[0].find_element(By.CLASS_NAME, "search-results-title-desc")
                    products = desc_elem.text.strip()
                except:
                    products = ""

                try:
                    customer_link = cols[1].find_element(By.TAG_NAME, "a")
                    customer = customer_link.text.strip()
                except:
                    customer = cols[1].text.strip()

                publish_date = cols[2].text.strip()
                deadline = cols[3].text.strip()

                tenders.append({
                    "number": tender_number,
                    "link": tender_link,
                    "customer": customer,
                    "products": products,
                    "deadline": deadline,
                    "publish_date": publish_date
                })

            page += 1

    finally:
        driver.quit()

    return tenders


def main(max_items, output_file, to_db=False):
    tenders = parse_b2b_center_selenium(BASE_URL, max_items)
    if max_items:
        tenders = tenders[:max_items]

    if to_db:
        save_to_sqlite(tenders, db_file=output_file)
    else:
        save_to_csv(tenders, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Приложение загрузки тендеров с сайта {BASE_URL}",
                                     epilog="Пример использования:\n  python main.py --max 20 --output databaseDB.db --db")

    # Аргументы args
    parser.add_argument("--max", type=int, default=50, help="Число тендеров для загрузки.")
    parser.add_argument("--output", type=str, default="tenders.csv",
                        help="Название и формат файла для сохранения результатов.")
    parser.add_argument("--db", action="store_true", help="Флаг БД. При его наличии создается файл формата .db")

    # Объект args
    args = parser.parse_args()
    main(args.max, args.output, args.db)
