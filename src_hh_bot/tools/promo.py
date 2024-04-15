import random
import string


def gen_id_promocode(len_: int) -> str:

    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    id_ = "".join(random.choice(letters) for _ in range(len_))
    return id_

