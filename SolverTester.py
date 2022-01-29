import numpy as np
from Wordle import Wordle, score, Tip
from Solver import Solver
from words import answers
import time

start_time = time.time()

guess_count = np.zeros(7, int)  # 6 potential guesses, plus 1 more for game over

num_guesses_for_hardest_word = -1
hardest_word = None
first_guess = "rebut"
all_correct = [Tip.CORRECT, Tip.CORRECT, Tip.CORRECT, Tip.CORRECT, Tip.CORRECT]

for word in answers:
    # wordle = Wordle("tuber")
    wordle = Wordle(word)
    solver = Solver()
    num_guesses = 1
    random_guess = first_guess

    while solver.remaining_answers() > 1:
        # print(f"guess {num_guesses}: {random_guess}")
        tips = score(wordle.answer, random_guess)
        solver.update_guess(random_guess, tips)

        if tips != all_correct:
            num_guesses += 1
            random_guess = solver.random_guess()

    if num_guesses >= num_guesses_for_hardest_word:
        hardest_word = wordle.answer
    if num_guesses > 7:
        num_guesses = 7  # is a loss
    guess_count[num_guesses - 1] += 1
print(guess_count)
print("--- %s seconds ---" % (time.time() - start_time))
print(f"the hardest word was: {hardest_word}")
# [  1  39 189 438 615 522 511]
# --- 12.554895639419556 seconds ---
# the hardest word was: shave
