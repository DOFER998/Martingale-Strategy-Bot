import random

from tg_bot.data.database import get_coeff


def random_number():
    number = random.uniform(get_coeff()['0'], get_coeff()['1'])
    return f'{number:.2f}'
