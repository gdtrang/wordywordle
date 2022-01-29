import pandas as pd

from Wordle import Wordle, Tip
from words import answers, guesses


def replace_char_at_position(string, position, character) -> str:
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
        self.known_letters = set([])  # loosely used
        self.known_letter_and_location = set([])
        self.known_pattern = r"....."
        self.letters = 'abcdefghijklmnopqrstuvwxyz'

    def update_guess(self, guess_word, score):
        for i, (tip, char) in enumerate(zip(score, guess_word)):
            if tip == Tip.MISSING:
                if char not in self.known_letters and char not in self.known_letter_and_location:
                    self.missing_letters.add(char)
            elif tip == Tip.WRONG_LOC:
                self.known_letters.add(char)
            if tip == Tip.CORRECT:
                self.known_letter_and_location.add(char)
                self.known_pattern = replace_char_at_position(self.known_pattern, i, char)

        guesses = "".join(self.missing_letters)
        pattern = self.known_pattern
        if self.missing_letters:  # is not empty
            pattern = self.known_pattern.replace(".", f"[^{guesses}]")
        # print(f"regex pattern: {pattern}")
        self.valid_solutions_df = self.valid_solutions_df.loc[self.valid_solutions_df.word.str.match(pattern)]
        if self.remaining_answers() == 0:
            raise Exception("no possible answers are remaining")
        if self.remaining_answers() != 1:
            self.valid_solutions_df = self.valid_solutions_df.loc[self.valid_solutions_df["word"] != guess_word]

    def random_guess(self) -> str:
        return self.valid_solutions_df.sample(1).word.values[0]

    def remaining_answers(self):
        return self.valid_solutions_df.shape[0]
