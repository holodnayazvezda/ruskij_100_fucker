DANIIL_COOKIE = "russkij100_uid=AZuoYEypc8erQbMOYwPKzA.D4Q1QGV0Hws8-IOx0CqE0_HiFKkpoamaG39QnlXfEcI"



def get_headers():
    HEADERS = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "Host": "test.russkij100.ru",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", # Fake
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": 'russkij100_uid=AZutE52XfI6gqsv5rEDPgw.wRj5RL69kkiOTZQNQXYHpAU6BmP4NVyN7YLuIbSFnrc'
    }
    return HEADERS


ege_test_url = "https://test.russkij100.ru/workout/{}?size=10"
test_task_submit_url = "https://test.russkij100.ru/api2/addTestAnswer?id={}&n=1"
test_delete_url = "https://test.russkij100.ru/api3/testResult?id={}"
