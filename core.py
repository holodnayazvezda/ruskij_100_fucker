import time
import requests
import re
import json

from bs4 import BeautifulSoup
from random import randint

from config import HEADERS
from tasks_json_parsers.task12 import get_json_payload_for_task_12

test_url = "https://test.russkij100.ru/workout/12d?size=10"
test_task_submit_url = "https://test.russkij100.ru/api2/addTestAnswer?id={}&n=1"
test_delete_url = "https://test.russkij100.ru/api3/testResult?id={}"

def get_test_info():
    r = requests.get(
        url=test_url,
        headers=HEADERS
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


def delete_info_about_test(test_id: int):
    url = test_delete_url.format(test_id)
    r = requests.delete(
        url=url,
        headers=HEADERS
    )
    if r.status_code != 200:
        print(f"Не удалось удалить test id = {test_id}")


def get_answers_on_test(test_id: int, question_ids: list[int]):
    f = open('answers/12.json', 'r', encoding='utf-8')
    answers = json.loads(f.read())
    f.close()
    url = test_task_submit_url.format(test_id)
    start_timestamp = int(time.time() * 1000) - 2000 * 1000
    for i, q_id in enumerate(question_ids, start=1):
        if q_id in answers:
            continue
        q_id = str(q_id)
        end_timestamp = start_timestamp + 200 * 1000
        requests_payload_text = get_json_payload_for_task_12(
            start_timestamp, end_timestamp,
            test_id,
            i, "2865",
            "12"
        )

        if i != 10:
            r = requests.post(
                url=url,
                headers=HEADERS,
                data=requests_payload_text
            )
            if r.status_code != 200:
                raise Exception(f"Не удалось получить ответ на задание {q_id}, status code: {r.status_code}")
            response_json = r.json()
            correct_answer = response_json['answers'][0]["correctAnswer"].replace(' ', '')
            answers[q_id] = correct_answer
    delete_info_about_test(test_id)
    print("Парсинг завершен! Текущее количество ответов:", len(answers))
    f = open('answers/12.json', 'w', encoding='utf-8')
    f.write(json.dumps(answers, ensure_ascii=False))
    f.close()


def solve_test_using_stored_answers(test_id: int, question_ids: list[int]):
    f = open('answers/12.json', 'r', encoding='utf-8')
    answers = json.loads(f.read())
    f.close()
    url = test_task_submit_url.format(test_id)
    start_timestamp = int(time.time() * 1000) - 2000 * 1000
    for i, q_id in enumerate(question_ids, start=1):
        if q_id in answers:
            continue
        q_id = str(q_id)
        need_to_save_answer = False
        if q_id not in answers:
            answer = "135"
            need_to_save_answer = True
        else:
            answer = answers[q_id]
        end_timestamp = start_timestamp + 200 * 1000
        requests_payload_text = get_json_payload_for_task_12(
            start_timestamp, end_timestamp,
            test_id,
            i, q_id,
            answer
        )
        if i == 10:
            time_to_sleep = (18 + randint(2, 7)) * 60
            print(f'Создаем иммитацию честности, сплю {time_to_sleep}')
            time.sleep(time_to_sleep)
        r = requests.post(
            url=url,
            headers=HEADERS,
            data=requests_payload_text
        )
        if r.status_code != 200:
            raise Exception(f"Не удалось отправить ответ на задание {q_id}, status code: {r.status_code}")
        if need_to_save_answer:
            print(f'Дополнительно сохраняю в базу задание №{q_id}')
            response_json = r.json()
            correct_answer = response_json['answers'][0]["correctAnswer"].replace(' ', '')
            answers[q_id] = correct_answer
            f = open('answers/12.json', 'w', encoding='utf-8')
            f.write(json.dumps(answers, ensure_ascii=False))
            f.close()
        else:
            print(f"Решено задание {i}, №{q_id}")

def solve_tets():
    test_html = get_test_info()
    test_id, answer_nums = parse_test_hrml(test_html)
    # get_answers_on_test(test_id, answer_nums)
    solve_test_using_stored_answers(test_id, answer_nums)


if __name__ == "__main__":
    solve_tets()
    # for i in range(40):
    #     solve_tets()
    #     time.sleep(5)