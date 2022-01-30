from Solver import Solver
from Wordle import Tip


def convert_to_enum(tips) -> list[Tip]:
    result = []
    for char in tips:
        assert char in ("=", "+", "-")
        if char == "=":
            result.append(Tip.CORRECT)
        elif char == "+":
            result.append(Tip.WRONG_LOC)
        elif char == "-":
            result.append(Tip.MISSING)
        else:
            print(f"something went wrong, received {char}")
    return result


solver = Solver()
print("enter = for correct letters, + for existing but wrong location, and - for not found (any more)")
random_guess = "savor"
while solver.remaining_answers() >= 2:
    print(f"solver is guessing: {random_guess}")
    tips = convert_to_enum(input())
    solver.update_guess(random_guess, tips)
    random_guess = solver.random_guess()

print(f"Answer must be: {solver.random_guess()}")

