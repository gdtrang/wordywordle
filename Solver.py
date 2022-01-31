import pandas as pd

from Wordle import Tip
from words import answers


def replace_char_at_position(string, position, character) -> str:
    return string[:position] + character + string[position + 1:]


all_correct = [Tip.CORRECT, Tip.CORRECT, Tip.CORRECT, Tip.CORRECT, Tip.CORRECT]


class Solver:
    def __init__(self):
        self.valid_solutions_df = pd.DataFrame(answers)
        self.valid_solutions_df.columns = ["word"]

        self.missing_letters = set([])
        self.known_letters = set([])
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
            elif tip == Tip.WRONG_LOC:
                #  remove words with letter at this location
                self.known_letters.add(char)
                pattern = replace_char_at_position(self.known_pattern, i, f"[^{char}]")
                self.valid_solutions_df = self.valid_solutions_df.loc[self.valid_solutions_df.word.str.match(pattern)]
                # remove words without this letter
                self.valid_solutions_df = self.valid_solutions_df.query(f"word.str.contains('{char}')", engine='python')
        # Separated out missing because guesses like "kappa" against "humph" would note that p is missing first
        # So it would remove "humph"
        for i, (tip, char) in enumerate(zip(tips, guess_word)):
            if tip == Tip.MISSING:
                if char not in self.known_letters and char not in self.known_letter_and_location:
                    self.missing_letters.add(char)

        #  Remove words with letters not in correct position
        pattern = self.known_pattern
        missing_letters_joined = "".join(self.missing_letters)
        if self.missing_letters:  # is not empty
            pattern = pattern.replace(".", f"[^{missing_letters_joined}]")
        self.valid_solutions_df = self.valid_solutions_df.loc[self.valid_solutions_df.word.str.match(pattern)]

        if self.remaining_answers() == 0:
            raise Exception("no possible answers are remaining")
        if self.remaining_answers() != 1:
            self.valid_solutions_df = self.valid_solutions_df.loc[self.valid_solutions_df["word"] != guess_word]
        if remaining_answers_at_start == self.remaining_answers():
            print(f"was given {guess_word} and it had no improvement and there are {self.remaining_answers()} remaining")

    #  quick helper functions
    def random_guess(self) -> str:
        return self.valid_solutions_df.sample(1).word.values[0]

    def letter_elimination_guess(self) -> str:
        known_letters_set = set.union(self.known_letters, self.known_letter_and_location)
        letters = "|".join(known_letters_set)
        fewer_words_all = self.valid_solutions_df.query(f"word.str.contains('{letters}') == False", engine='python')
        letters = "|".join(self.known_letter_and_location)
        fewer_words_some = self.valid_solutions_df.query(f"word.str.contains('{letters}') == False", engine='python')
        if fewer_words_all.shape[0] > 0:
            return fewer_words_all.sample(1).word.values[0]
        elif fewer_words_some.shape[0] > 0:
            return fewer_words_some.sample(1).word.values[0]
        else:
            return self.random_guess()

    def remaining_answers(self):
        return self.valid_solutions_df.shape[0]
