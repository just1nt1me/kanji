import pandas as pd
import streamlit as st
from nltk.corpus import wordnet
from util import wordnet_similarity

# Define the CSV file list and JLPT level list
csv_list = ["n1.csv", "n2.csv", "n3.csv", "n4.csv", "n5.csv"]
level_list = ["n5", "n4", "n3", "n2", "n1"]

class KanjiLevelTest:
    def __init__(self):
        self.load_state()

    def load_state(self):
        # Initialize or load session state variables
        if 'current_level' not in st.session_state:
            st.session_state.current_level = 0

        if 'current_kanji_index' not in st.session_state:
            st.session_state.current_kanji_index = 0

        if 'score' not in st.session_state:
            st.session_state.score = 0

        if 'total' not in st.session_state:
            st.session_state.total = 0

        if 'answered' not in st.session_state:
            st.session_state.answered = False

        if 'message' not in st.session_state:
            st.session_state.message = ""

        if 'next_button_clicked' not in st.session_state:
            st.session_state.next_button_clicked = False

    def load_deck(self):
        # Check if the deck has already been loaded for this session
        if 'deck' not in st.session_state:
            st.session_state.deck = {}
            for csv in csv_list:
                level = csv.split(".")[0]
                df = pd.read_csv(csv)
                st.session_state.deck[level] = df.sample(n=10)

    def test_type(self):
        self.type = st.radio("Practice reading (j) or definition (e)?", ["j", "e"])

    def test(self):
        if st.session_state.current_level < len(level_list):
            level = level_list[st.session_state.current_level]
            kanji = st.session_state.deck[level].iloc[st.session_state.current_kanji_index]

            st.header(f"Let's start the {level} test")
            st.write(f"Kanji: {kanji['expression']}")

            if not st.session_state.answered:
                answer = st.text_input(f"Your answer for {kanji['expression']}:", key=f"{kanji['expression']}_{level}_input")
                check_button = st.button("Check", key=f"check_button_{kanji['expression']}_{level}")
                next_button = st.button("Next Question", key=f"next_button_{kanji['expression']}_{level}")


                if check_button:
                    if answer.lower() == 'exit':
                        st.stop()

                    if self.type == "j":
                        if answer == kanji['reading']:
                            st.session_state.message = f"{answer} is correct"
                            st.session_state.score += 1
                        else:
                            st.session_state.message = f"{answer} is incorrect. {kanji['expression']} is read {kanji['reading']}"

                    if self.type == "e":
                        similarity = wordnet_similarity(answer, kanji['meaning'])
                        if similarity > 0.7:
                            st.session_state.message = f"{answer} is correct. {kanji['expression']} means {kanji['meaning']}"
                            st.session_state.score += 1
                        else:
                            st.session_state.message = f"{answer} is incorrect. {kanji['expression']} means {kanji['meaning']}"

                    st.session_state.answered = True

            st.write(st.session_state.message)
            next_button

            if st.session_state.answered:
                st.session_state.current_kanji_index += 1
                st.session_state.message = ""
                st.session_state.answered = False

                if st.session_state.current_kanji_index == 10:
                    if st.session_state.score >= 5:
                        st.write(f"You passed {level} with {st.session_state.score}/10 correct")
                        st.session_state.total += st.session_state.score
                        st.session_state.score = 0
                        st.session_state.current_level += 1
                        st.session_state.current_kanji_index = 0
                    else:
                        st.write(f"You failed {level} with {st.session_state.score}/10")
                        st.write(f"Study {level} kanji!")
                        st.stop()

        if st.session_state.current_level >= len(level_list):
            st.success(f"Total Score: {st.session_state.total}/50 correct")
            st.stop()

if __name__ == "__main__":
    st.title("Kanji Level Test")
    test_instance = KanjiLevelTest()
    test_instance.load_deck()
    test_instance.test_type()
    test_instance.test()
