from Solver import Solver

if __name__ == '__main__':

    solver = Solver()
    while solver.remaining_answers() >= 2:
        solver.update_guess(solver.random_guess())
        print(solver.remaining_answers())
    print(f"solver is guessing: {solver.random_guess()}")
    print(f"answer is: {solver.wordle.answer}")
