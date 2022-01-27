import pandas as pd

from Wordle import Wordle, Tip
from words import answers, guesses


def string_replace(string, position, character) -> str:
    return string[:position] + character + string[position + 1:]


class Solver:
    def __init__(self):
        self.valid_solutions_df = pd.DataFrame(answers)
        self.valid_solutions_df.columns = ["word"]
        self.valid_guesses_df = pd.DataFrame(guesses)
        self.valid_guesses_df.columns = ["word"]
        self.all_df = pd.concat([self.valid_solutions_df, self.valid_guesses_df])
        self.num_answers = len(answers)
        self.all_guesses = len(self.all_df)
        self.words = open("wordle-12k.txt", "r").read().splitlines()

        self.missing_letters = set([])
        self.known_letters = set([])  # not actually used yet
        self.known_pattern = r"....."
        self.letters = 'abcdefghijklmnopqrstuvwxyz'
        self.wordle = Wordle()

    def update_guess(self, guess_word):
        print(f"guess: {guess_word}")
        guess = self.wordle.guess(guess_word)

        for i, (tip, char) in enumerate(zip(guess, guess_word)):
            if tip == Tip.MISSING:
                if char not in self.known_letters:
                    self.missing_letters.add(char)
            elif tip == Tip.WRONG_LOC:
                self.known_letters.add(char)
            if tip == Tip.CORRECT:
                self.known_pattern = string_replace(self.known_pattern, i, char)

        print(f"missing letters after guess: {self.missing_letters}")

        guesses = "".join(self.missing_letters)
        pattern = self.known_pattern.replace(".", f"[^{guesses}]")
        print(f"regex pattern: {pattern}")
        self.valid_solutions_df = self.valid_solutions_df.loc[self.valid_solutions_df.word.str.match(pattern)]

    def random_guess(self) -> str:
        answers_remaining = self.valid_solutions_df.shape[0]
        print(f"possible answers remaining: {answers_remaining}")
        return self.valid_solutions_df.sample(1).word.values[0]

    def remaining_answers(self):
        return self.valid_solutions_df.shape[0]
