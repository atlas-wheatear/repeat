import string
from wheatear_repeat import repeat

@repeat(
    string.ascii_letters + string.digits + '-_}',
    30
)
def get_flag(candidate_string: str) -> bool:
    FLAG = 'HTB{fl4gs-4r3_fun}'
    # this is a silly example
    return FLAG.startswith(candidate_string)

print(
    get_flag(initial='HTB{')
)
