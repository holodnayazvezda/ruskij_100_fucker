DANIIL_COOKIE = "russkij100_uid=AZuoYEypc8erQbMOYwPKzA.D4Q1QGV0Hws8-IOx0CqE0_HiFKkpoamaG39QnlXfEcI"

ANSWERS_GETTER_COOKIE = [
    "russkij100_uid=AZuqzITwdlqpSkyEtkyB-A.uSU2XXBDSuUpZGelBTGkoJFdntGBkkK_aUWEpn0VIuw",
    "russkij100_uid=AZus3ofRdb61uRBxuuCkhQ.TgABiUjAsqy4J5mMCT12CNItCAWkeYKbi1SktN04VW0",
    "russkij100_uid=AZus4C4BcHOdZUrLZZgp6Q.jb1H0vm8PLWfUkuZ4OdzrwXKbDrB1u8oaJ7WFi3UYD8",
    "russkij100_uid=AZus4U_6cxC8jI_JmjKhlw.meIQR-DO5YAqgovWKNtVshSr_X7KEn7PRVDeH_QPgSA",
    "russkij100_uid=AZus5PBWcvyMU89sEndsPg.wTUTIiP9FHhIFYV87kj0xjpVCaQUtYZT-8Jq0cICd-0"
]
amount_of_requests = 0


def get_headers():
    global amount_of_requests
    amount_of_requests += 1
    HEADERS = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "Host": "test.russkij100.ru",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", # Fake
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": ANSWERS_GETTER_COOKIE[amount_of_requests % 3]
    }
    return HEADERS


ege_test_url = "https://test.russkij100.ru/workout/{}?size=10"
test_task_submit_url = "https://test.russkij100.ru/api2/addTestAnswer?id={}&n=1"
test_delete_url = "https://test.russkij100.ru/api3/testResult?id={}"
