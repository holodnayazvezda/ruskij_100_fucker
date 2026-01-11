import json


def get_json_payload_for_task_12(
    start_timestamp: int,
    end_timestamp: int,
    test_id: int,
    question_number: int,
    question_id: str,
    answer_to_send: str
) -> str:
    payload_dict = {
        "startTimestamp": start_timestamp,
        "endTimestamp": end_timestamp,
        "testResultId": test_id,
        "answers": [
            {
                "number": question_number,
                "answer": answer_to_send,
                "pointAnswer": {
                    "questionId": question_id,
                    "questionNumber": question_number,
                    "items": []
                }
            }
        ],
        "forceFinish": False
    }
    return json.dumps(payload_dict)
