import pandas as pd

from Wordle import Tip
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

        self.missing_letters = set([])
        self.known_letters = set([])  # loosely used
        self.known_letter_and_location = set([])
        self.known_pattern = r"....."

        self.guess = ['.'] * 5

    def update_guess(self, guess_word, tips):
        remaining_answers_at_start = self.remaining_answers()
        if remaining_answers_at_start == 1:
            print("Not attempting to solve as there is 1 answer remaining")
            return

        for i, (tip, char) in enumerate(zip(tips, guess_word)):
            if tip == Tip.CORRECT:
                self.known_letter_and_location.add(char)
                self.known_pattern = replace_char_at_position(self.known_pattern, i, char)
                self.valid_solutions_df = self.valid_solutions_df.loc[self.valid_solutions_df.word.str.match(
                    self.known_pattern)]
            elif tip == Tip.WRONG_LOC:
                self.known_letters.add(char)
                #  remove words with letter at this location
                pattern = replace_char_at_position(self.known_pattern, i, f"[^{char}]")
                # remove missing letter
                self.valid_solutions_df = self.valid_solutions_df.loc[self.valid_solutions_df.word.str.match(pattern)]
                # remove words without this letter (unnecessary?)
                self.valid_solutions_df = self.valid_solutions_df.query(f"word.str.contains('{char}')", engine='python')
        # Separated out missing because guesses like "kappa" against "humph" would note that p is missing first
        # So it word remove "humph"
        for i, (tip, char) in enumerate(zip(tips, guess_word)):
            if tip == Tip.MISSING:
                if char not in self.known_letters and char not in self.known_letter_and_location:
                    if char not in self.missing_letters:
                        self.valid_solutions_df = self.valid_solutions_df.query(f"word.str.contains('{char}') == False",
                                                                                engine='python')
                    self.missing_letters.add(char)

        missing_letters_joined = "".join(self.missing_letters)
        pattern = self.known_pattern
        if self.missing_letters:  # is not empty
            pattern = self.known_pattern.replace(".", f"[^{missing_letters_joined}]")

        # print(f"regex pattern: {pattern}")
        remaining_answers = self.remaining_answers()
        valid_solutions_df_before_match = self.valid_solutions_df
        self.valid_solutions_df = self.valid_solutions_df.loc[self.valid_solutions_df.word.str.match(pattern)]
        if self.remaining_answers() != remaining_answers:
            print(f"regex pattern: {pattern}")
            print("something is wrong")
            print(valid_solutions_df_before_match)
            print(self.valid_solutions_df)

        if self.remaining_answers() == 0:
            raise Exception("no possible answers are remaining")
        if self.remaining_answers() != 1:
            self.valid_solutions_df = self.valid_solutions_df.loc[self.valid_solutions_df["word"] != guess_word]
        if remaining_answers_at_start == self.remaining_answers():
            print(f"was given {guess_word} and it had no improvement and there are {self.remaining_answers()} remaining")
            print(tips)

    #  quick helper functions
    def random_guess(self) -> str:
        return self.valid_solutions_df.sample(1).word.values[0]

    def remaining_answers(self):
        return self.valid_solutions_df.shape[0]
