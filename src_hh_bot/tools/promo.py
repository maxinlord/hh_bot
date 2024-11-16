import random
import string


def gen_id_promocode(len_: int) -> str:
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return "".join(random.choice(letters) for _ in range(len_))
