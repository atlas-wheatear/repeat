import string
from wheatear_repeat import repeat

@repeat
def get_flag(candidate_string: str) -> bool:
    FLAG = 'HTB{fl4gs-4r3_fun}'
    # this is a silly example
    return FLAG.startswith(candidate_string)

get_flag.characters = string.ascii_letters + string.digits + '-_}',
get_flag.max_length = 30
get_flag.initial = 'HTB{'

print(get_flag())
