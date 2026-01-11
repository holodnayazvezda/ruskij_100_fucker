import json
import time
import requests

from config import test_delete_url, test_task_submit_url
from tasks_json_parsers.payloads_worker import get_json_payload_for_task_where_point_ans_needed, \
    get_json_payload_for_task_where_nothing_needed, get_json_payload_for_task_where_point_ans_and_extra_ans_needed
from utils.printer import print_to_file


def delete_info_about_test(test_id: int, headers: dict):
    url = test_delete_url.format(test_id)
    r = requests.delete(
        url=url,
        headers=headers
    )
    if r.status_code != 200:
        print_to_file(f"Не удалось удалить test id = {test_id}")


def get_answers_on_test(ege_num: int, task_type: str, test_id: int, question_ids: list[int], headers: dict):
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
                i, q_id,
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
            requests_payload_text = get_json_payload_for_task_where_point_ans_and_extra_ans_needed(
                start_timestamp, end_timestamp,
                test_id,
                i, q_id,
                "12"
            )

        if i != 10:
            r = requests.post(
                url=url,
                headers=headers,
                data=requests_payload_text
            )
            if r.status_code != 200:
                raise Exception(f"Не удалось получить ответ на задание {q_id}, status code: {r.status_code}")
            response_json = r.json()
            correct_answer = response_json['answers'][0]["correctAnswer"].replace(' ', '')
            answers[q_id] = correct_answer
    delete_info_about_test(test_id, headers)
    print_to_file("    Парсинг завершен! Текущее количество ответов:", len(answers))
    f = open(filename, 'w', encoding='utf-8')
    f.write(json.dumps(answers, ensure_ascii=False))
    f.close()
