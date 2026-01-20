DANIIL_COOKIE = "russkij100_uid=AZuoYEypc8erQbMOYwPKzA.D4Q1QGV0Hws8-IOx0CqE0_HiFKkpoamaG39QnlXfEcI"
ACYA_COOKIE = "russkij100_uid=AZvdmM1te8mEt9vrZcJXZw.fpS5GtQZ89NDSdyhjVtpLFnH1GIjcocq1UzMuFxtbsk"



def get_headers():
    HEADERS = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "Host": "test.russkij100.ru",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", # Fake
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": ACYA_COOKIE
    }
    return HEADERS


ege_test_url = "https://test.russkij100.ru/workout/{}?size=5"
test_task_submit_url = "https://test.russkij100.ru/api2/addTestAnswer?id={}&n=1"
test_delete_url = "https://test.russkij100.ru/api3/testResult?id={}"

SOLVER = 1
GETTER = 2
