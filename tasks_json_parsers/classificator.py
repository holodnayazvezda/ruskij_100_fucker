def classify_task(task_num: int) -> str:
    if task_num in [1, 2, 3, 4, 5, 6, 7,  23, 24, 25, 26]:
        return "nothing_needed"
    elif task_num in [9, 10, 11, 12, 13, 14, 15]:
        return "point_ans_needed"
    else:
        raise Exception(f"Задание ЕГЭ №{task_num} пока не поддерживается :(")