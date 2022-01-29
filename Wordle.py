import collections
import random
from words import answers
from enum import Enum, auto


class Tip(Enum):
    MISSING = auto()
    WRONG_LOC = auto()
    CORRECT = auto()


def score(secret, guess) -> list[Tip]:
    # All characters that are not correct go into the usable pool.
    pool = collections.Counter(s for s, g in zip(secret, guess) if s != g)
    # Create a first tentative score by comparing char by char.
    result = []
    for secret_char, guess_char in zip(secret, guess):
        if secret_char == guess_char:
            result.append(Tip.CORRECT)
        elif guess_char in secret and pool[guess_char] > 0:
            result.append(Tip.WRONG_LOC)
            pool[guess_char] -= 1
        else:
            result.append(Tip.MISSING)

    return result


class Wordle:
    max_guess = 6
    guess_count = 0

    def __init__(self, answer=None):
        # choose a random word from the answers list if not provided
        if answer is None:
            self.answer = random.choice(answers)
        else:
            self.answer = answer

    def guess(self, guess):
        return score(self.answer, guess)


# wordle = Wordle("trash")
# print(wordle.guess("trash"))
# print(f"answer was {wordle.answer}")

# print(score("sissy", "missy"))
