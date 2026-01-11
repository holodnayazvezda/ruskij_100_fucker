import re

import requests
from bs4 import BeautifulSoup

from config import get_headers


def get_test_info(test_url: str):
    r = requests.get(
        url=test_url,
        headers=get_headers()
    )
    if r.status_code != 200:
        raise Exception(f"Не удалось получить информацию по тесту, status code: {r.status_code}")
    return r.text


def parse_test_hrml(html: str) -> tuple[int, list[int]]:
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script')
    test_result_id = None

    for script in scripts:
        if script.string and 'TEST_RESULT_ID' in script.string:
            match = re.search(r'TEST_RESULT_ID\s*=\s*(\d+)', script.string)
            if match:
                test_result_id = int(match.group(1))
                break

    if not test_result_id:
        raise Exception("Ошибка: TEST_RESULT_ID не найден в HTML.")

    questions = soup.find_all("div", attrs={"data-question-id": True})
    question_ids = []
    for q in questions:
        q_id = q.get("data-question-id")
        if q_id:
            question_ids.append(int(q_id))

    return test_result_id, question_ids