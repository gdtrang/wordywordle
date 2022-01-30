from Solver import Solver
from Wordle import Wordle, score, Tip

all_correct = [Tip.CORRECT, Tip.CORRECT, Tip.CORRECT, Tip.CORRECT, Tip.CORRECT]

if __name__ == '__main__':
    # wordle = Wordle("tuber")
    wordle = Wordle("humph")
    solver = Solver()
    num_guesses = 1
    random_guess = "rebut"

    while solver.remaining_answers() > 1:
        print(f"guess {num_guesses}: {random_guess}")
        tips = score(wordle.answer, random_guess)
        solver.update_guess(random_guess, tips)

        # prepare for next iteration
        if tips != all_correct:
            num_guesses += 1
            random_guess = solver.random_guess()
            # print(f"answers remaining: {solver.remaining_answers()}")
        # print(solver.valid_solutions_df)

    print(f"answer is: {wordle.answer}")
    print(f"guesses required: {num_guesses}")

    if num_guesses > 6:
        print("game lost")

