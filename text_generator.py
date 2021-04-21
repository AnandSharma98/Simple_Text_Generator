from nltk.tokenize import regexp_tokenize
from collections import defaultdict
from random import choice, choices


pattern = r'[^\s]+'   # regular expression to not include whitespace characters such as newline, tab, space
filename = input()
with open(filename, 'r', encoding="utf-8") as f:   # file is corpus.txt will be given as input
    corpus = f.read()
    tokens = regexp_tokenize(corpus, pattern)      # it'll create list of tokens from corpus based on regex.
    n_tokens = len(tokens)

    """ it'll create trigrams 
    trigrams is nothing but a sequence of 3 words appeared somewhere in corpus provided
    here the first and second word will be head 
    and the third word will be tail
    eg winter is   (head)
       coming (tail)
     """
    trigrams = [(tokens[index] + " " + tokens[index+1], tokens[index + 2]) for index in range(n_tokens - 2)]

    """it'll create a inner dictionary whose keys would be the head from trigrams 
    and the values(that is a inner dict.) will have keys as tails and the value as no of frequency , that will
    tell how many times the trigram appeared with these head and tail combination"""

    trigram_dict = defaultdict(dict)
    for head, tail in trigrams:
        trigram_dict[head].setdefault(tail, 0)
        trigram_dict[head][tail] += 1

"""
we'll be generating 10 sentence with some constraints
first letter of the first word of each sentence should be capital plus it should not end like a sentence 
eg "My."  is not acceptable
each sentence length should be grater than equals to 5  
each sentence end like normal sentence with punctuations like "I'm a master from birth."


The beginning of the chain should be a randomly chosen head from the model(trigrams), not just any word from the
corpus.When predicting the next word, the model should be fed the concatenation of the last two tokens of the chain
separated by a space.
"""

word = choice(list(trigram_dict.keys()))
sentence_ending_punctuation = ["!", "?", "."]

# it'll generate 10 sentence as specified
for _ in range(10):
    # # first letter of the first word of each sentence should be capital plus it should not end like a sentence
    while not word.split()[0][0].isupper() or (word.split()[0][-1] in sentence_ending_punctuation):
        word = choice(list(trigram_dict.keys()))
    sentence = [word]

# it'll run till the condition mentioned for sentence gets satisfied
    while True:
        population = list(trigram_dict[word].keys())
        weights = list(trigram_dict[word].values())
        tail_r = choices(population, weights=weights)[0]
        word = word.split()[1] + " " + tail_r
        sentence.append(tail_r)

        # each sentence length should be grater than equals to 5
        if len(sentence) >= 4 and (sentence[-1][-1] in sentence_ending_punctuation):
            break

    print(' '.join(sentence))
    sentence = []
