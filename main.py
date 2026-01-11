import time

from config import ege_test_url, get_headers, SOLVER, GETTER
from core.test_solver import solve_test_using_stored_answers
from core.utils import get_test_info, parse_test_hrml
from core.test_answers_getter import get_answers_on_test
from tasks_json_parsers.classificator import classify_task
from utils.printer import print_to_file


def solve_tets(ege_num: int, launch_type = SOLVER):
    headers = get_headers()
    test_link_on_any_10 = ege_test_url.format(ege_num)
    task_type = classify_task(ege_num)
    test_html = get_test_info(test_link_on_any_10, headers)
    test_id, answer_nums = parse_test_hrml(test_html)
    if launch_type == GETTER:
        get_answers_on_test(ege_num, task_type, test_id, answer_nums, headers)
    else:
        solve_test_using_stored_answers(ege_num, task_type, test_id, answer_nums, headers, 20)

if __name__ == "__main__":
    TASK_NUMS_TO_SOLVE = {5: 1}
    working_type = SOLVER
    for ege_task_num, amount_of_circles in TASK_NUMS_TO_SOLVE.items():
        for i in range(amount_of_circles):
            print_to_file(f'Запуск ЕГЭ №{ege_task_num}, круг {i + 1}/{amount_of_circles}')
            solve_tets(ege_task_num, working_type)
            time.sleep(6)
        print_to_file(f'Завершено ЕГЭ №{ege_task_num} в количестве {amount_of_circles} кругов')
        time.sleep(35)
    # AMOUNT_OF_CIRCLES = 70
    # for _ in range(AMOUNT_OF_CIRCLES):
    #     solve_tets(EGE_TASK_NUM)
    #     time.sleep(5)
    # for i in range(40):
    #     solve_tets()
    #     time.sleep(5)
