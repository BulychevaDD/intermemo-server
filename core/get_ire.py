import math

from models.db import Card


def get_ire(card: Card, quality: int) -> [int, int, float]:
    if quality < 3:
        return 1, 0, card.previous_easy_factor

    repetitions = card.repetitions + 1

    if card.repetitions == 0:
        interval = 1
    elif card.repetitions == 1:
        interval = 6 // card.difficulty
    else:
        interval = math.ceil(card.previous_interval * card.previous_easy_factor)

    easy_factor = card.previous_easy_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

    if easy_factor < 1.3:
        easy_factor = 1.3

    return interval, repetitions, easy_factor
