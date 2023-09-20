import pandas as pd
import random
import sys
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from util import wordnet_similarity

csv_list = ["n1.csv", "n2.csv", "n3.csv", "n4.csv", "n5.csv"]
level_list = ["n5", "n4", "n3", "n2", "n1"]


class Test:
    def __init__(self):
        self.deck = {}

    # create a deck with 5 mini-decks, one for each JLPT level with 10 kanji each
    def get_deck(self):
        for csv in csv_list:
            level = csv.split(".")[0]
            df = pd.DataFrame(pd.read_csv(csv))
            self.deck[level] = df.sample(n=10)


    def test_type(self):
        self.type = input("Practice reading (j) or definition (e)? Enter j/e: ")
        if self.type not in ["j", "e"]:
            raise ValueError("Invalid input")


    # test user's ability to read kanji, input is ひらがな
    def test(self, kanji, score):
        if self.type == "j":
            for index, row in kanji.iterrows():
                answer = input(f"{row['expression']} (type 'exit' to quit): ")

                # check if user wants to exit
                if answer.lower() == 'exit':
                    sys.exit()

                if answer == row['reading']:
                    print(f"{answer} is correct")
                    score += 1
                else:
                    print(f"{answer} is incorrect. {row['expression']} is read {row['reading']}")

        if self.type == "e":
            # show kanji, allow user input, score semantic similarity
            for index, row in kanji.iterrows():
                answer = input(f"{row['expression']} (type 'exit' to quit): ")

                # Check if the user wants to exit
                if answer.lower() == 'exit':
                    sys.exit()

                # Compute WordNet-based similarity between user input and correct answer
                # TODO: check similarity for each comma separated string...
                similarity = wordnet_similarity(answer, row['meaning'])

                if similarity > 0.7:  # Adjust the threshold as needed
                    print(f"{answer} is correct. {row['expression']} means {row['meaning']}")
                    score += 1
                else:
                    print(f"{answer} is incorrect. {row['expression']} means {row['meaning']}")

        return score

    # user takes test level by level until failing score
    def take_test(self):
        total_score = 0
        for level in level_list:
            print(f"Let's start the {level} test")
            score = 0
            kanji = self.deck[level]
            score = self.test(kanji, score)  # Call the instance method 'test'
            print(f"{score}/10 correct")
            total_score += score
            if score < 5:
                sys.exit(f"You should study from {level}")
        print(f"{total_score}/50 correct")

if __name__ == "__main__":
    test_instance = Test()
    test_instance.get_deck()
    test_instance.test_type()
    test_instance.take_test()
