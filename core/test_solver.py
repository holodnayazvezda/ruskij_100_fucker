import json
import time
import requests

from random import randint

from config import test_task_submit_url
from tasks_json_parsers.payloads_worker import get_json_payload_for_task_where_point_ans_needed, \
    get_json_payload_for_task_where_nothing_needed, get_json_payload_for_task_where_point_ans_and_extra_ans_needed


def solve_test_using_stored_answers(
        ege_num: int, task_type: str,
        test_id: int, question_ids: list[int], headers: dict,
        time_to_sleep_onq1_task: int
):
    time_to_sleep_onq1_task += randint(1, 20)
    filename = f'answers/{ege_num}.json'
    f = open(filename, 'r', encoding='utf-8')
    answers = json.loads(f.read())
    url = test_task_submit_url.format(test_id)
    start_timestamp = int(time.time() * 1000) - 2000 * 1000
    for i, q_id in enumerate(question_ids, start=1):
        if q_id in answers:
            continue
        q_id = str(q_id)
        need_to_save_answer = False
        if q_id not in answers:
            answer = "ожидают"
            need_to_save_answer = True
        else:
            answer = answers[q_id]
            answer = answer.replace('(', '').replace(')', '').split('|')[0]
        end_timestamp = start_timestamp + 200 * 1000
        if task_type == "point_ans_needed":
            requests_payload_text = get_json_payload_for_task_where_point_ans_needed(
                start_timestamp, end_timestamp,
                test_id,
                i, q_id,
                answer
            )
        elif task_type == "nothing_needed":
            requests_payload_text = get_json_payload_for_task_where_nothing_needed(
                start_timestamp, end_timestamp,
                test_id,
                i,
                answer
            )
        else:
            requests_payload_text = get_json_payload_for_task_where_point_ans_and_extra_ans_needed(
                start_timestamp, end_timestamp,
                test_id,
                i, q_id,
                answer
            )
        if i == 5:
            time_to_sleep = time_to_sleep_onq1_task * randint(7, 14)
            print(f'Создаем иммитацию честности, сплю {time_to_sleep}')
            time.sleep(time_to_sleep)
        r = requests.post(
            url=url,
            headers=headers,
            data=requests_payload_text
        )
        if r.status_code != 200:
            raise Exception(f"Не удалось отправить ответ на задание {q_id}, status code: {r.status_code}")
        if need_to_save_answer:
            print(f'Дополнительно сохраняю в базу задание №{q_id}')
            response_json = r.json()
            correct_answer = response_json['answers'][0]["correctAnswer"].replace(' ', '')
            answers[q_id] = correct_answer
            f = open(filename, 'w', encoding='utf-8')
            f.write(json.dumps(answers, ensure_ascii=False))
            f.close()
        else:
            print(f"Решено задание {i}, №{q_id}")
