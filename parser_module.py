import requests
import json
import logging
import sqlite3
import asyncio


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, filename='logs/parser_module.log',
    filemode='w', 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


conn = sqlite3.connect('data/database.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS vacancies (
    id INTEGER PRIMARY KEY,
    datetime TEXT DEFAULT CURRENT_TIMESTAMP,
    vacancy_count INTEGER,
    change INTEGER DEFAULT 0
)""")
conn.commit()
conn.close()


try:
    with open("query.json") as f:
        query = json.load(f)
except FileNotFoundError:
    logger.error("File query.json not found")
    query = {}


async def get_json_from_site() -> tuple[list, int]:
    request_result = requests.post(
        "https://dracula.robota.ua/?q=getPublishedVacanciesList", 
        json=query,
        headers={'Content-Type': 'application/json'}
    )
    if request_result.status_code >= 300:
        logger.error(f"Request failed with status code {request_result.status_code}")
        return [], -1
    json_data = request_result.json()
    return json_data['data']['publishedVacancies']['items'], json_data['data']['publishedVacancies']['totalCount']


async def run_hourly_parse_site():
    while True:
        list_of_vacancies, total_vacancies = await get_json_from_site()
        if total_vacancies == -1:
            await asyncio.sleep(60)
            continue
        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT vacancy_count FROM vacancies ORDER BY id DESC LIMIT 1")
        last_vacancy_count = cursor.fetchone()
        if last_vacancy_count is None:
            last_vacancy_count = 0
        else:
            last_vacancy_count = last_vacancy_count[0]
        cursor.execute("INSERT INTO vacancies (vacancy_count, change) VALUES (?, ?)", (total_vacancies, total_vacancies - last_vacancy_count))
        conn.commit()
        conn.close()
        await asyncio.sleep(3600)
