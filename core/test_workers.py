import json
import time
from random import randint

import requests

from config import test_delete_url, HEADERS, test_task_submit_url
from tasks_json_parsers.task12 import get_json_payload_for_task_where_point_ans_needed, \
    get_json_payload_for_task_where_nothing_needed


def delete_info_about_test(test_id: int):
    url = test_delete_url.format(test_id)
    r = requests.delete(
        url=url,
        headers=HEADERS
    )
    if r.status_code != 200:
        print(f"Не удалось удалить test id = {test_id}")


def get_answers_on_test(ege_num: int, task_type: str, test_id: int, question_ids: list[int]):
    filename = f'answers/{ege_num}.json'
    f = open(filename, 'r', encoding='utf-8')
    answers = json.loads(f.read())
    f.close()
    url = test_task_submit_url.format(test_id)
    start_timestamp = int(time.time() * 1000) - 2000 * 1000
    for i, q_id in enumerate(question_ids, start=1):
        if q_id in answers:
            continue
        q_id = str(q_id)
        end_timestamp = start_timestamp + 200 * 1000
        if task_type == "point_ans_needed":
            requests_payload_text = get_json_payload_for_task_where_point_ans_needed(
                start_timestamp, end_timestamp,
                test_id,
                i, "2865",
                "12"
            )
        elif task_type == "nothing_needed":
            requests_payload_text = get_json_payload_for_task_where_nothing_needed(
                start_timestamp, end_timestamp,
                test_id,
                i,
                "12"
            )
        else:
            raise Exception("Непредсказуемый тип задания")

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
    f = open(filename, 'w', encoding='utf-8')
    f.write(json.dumps(answers, ensure_ascii=False))
    f.close()


# def solve_test_using_stored_answers(test_id: int, question_ids: list[int]):
#     f = open('answers/12.json', 'r', encoding='utf-8')
#     answers = json.loads(f.read())
#     f.close()
#     url = test_task_submit_url.format(test_id)
#     start_timestamp = int(time.time() * 1000) - 2000 * 1000
#     for i, q_id in enumerate(question_ids, start=1):
#         if q_id in answers:
#             continue
#         q_id = str(q_id)
#         need_to_save_answer = False
#         if q_id not in answers:
#             answer = "135"
#             need_to_save_answer = True
#         else:
#             answer = answers[q_id]
#         end_timestamp = start_timestamp + 200 * 1000
#         requests_payload_text = get_json_payload_for_task_12(
#             start_timestamp, end_timestamp,
#             test_id,
#             i, q_id,
#             answer
#         )
#         if i == 10:
#             time_to_sleep = (18 + randint(2, 7)) * 60
#             print(f'Создаем иммитацию честности, сплю {time_to_sleep}')
#             time.sleep(time_to_sleep)
#         r = requests.post(
#             url=url,
#             headers=HEADERS,
#             data=requests_payload_text
#         )
#         if r.status_code != 200:
#             raise Exception(f"Не удалось отправить ответ на задание {q_id}, status code: {r.status_code}")
#         if need_to_save_answer:
#             print(f'Дополнительно сохраняю в базу задание №{q_id}')
#             response_json = r.json()
#             correct_answer = response_json['answers'][0]["correctAnswer"].replace(' ', '')
#             answers[q_id] = correct_answer
#             f = open('answers/12.json', 'w', encoding='utf-8')
#             f.write(json.dumps(answers, ensure_ascii=False))
#             f.close()
#         else:
#             print(f"Решено задание {i}, №{q_id}")
