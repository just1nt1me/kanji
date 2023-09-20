import pandas as pd
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

csv_list = ["n1.csv", "n2.csv", "n3.csv", "n4.csv", "n5.csv"]

# clean up csv and output
def clean_csv(csv):
    level = csv.split('.')[0]
    df = pd.DataFrame(pd.read_csv(csv))
    df = df.drop_duplicates(subset=["expression"])
    df.tags = level
    df = df[['expression', 'reading', 'meaning', 'tags']]
    df.to_csv(csv, index=False)

def main():
    for csv in csv_list:
        clean_csv(csv)

# Define a function to compute WordNet-based similarity
def wordnet_similarity(user_input, correct_answer):
    user_tokens = word_tokenize(user_input)
    answer_tokens = word_tokenize(correct_answer)

    # Initialize a list to store individual word similarities
    word_similarities = []

    for user_word in user_tokens:
        max_similarity = 0  # Initialize max similarity for the current user word

        for answer_word in answer_tokens:
            user_synsets = wordnet.synsets(user_word)
            answer_synsets = wordnet.synsets(answer_word)

            if user_synsets and answer_synsets:
                similarity = max(
                    s1.wup_similarity(s2) for s1 in user_synsets for s2 in answer_synsets
                )

                if similarity > max_similarity:
                    max_similarity = similarity

        word_similarities.append(max_similarity)

    # Calculate the average similarity across all user words
    if word_similarities:
        average_similarity = sum(word_similarities) / len(word_similarities)
        return average_similarity
    else:
        return 0


if __name__ == "__main__":
    main()
