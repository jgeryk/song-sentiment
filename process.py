from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
import re
import os
import simple-averaging
import naivebayes

lmtzr = WordNetLemmatizer()
NEG_TAG = '-'
POS_TAG = '+'
NEU_TAG = '0'
PATH_TO_TRAIN = os.getcwd() + '/lyrics_annotated/train/'

def read_lyrics_from_file(file):
    words = []
    f = open(file)
    for line in f:
        words.append(line)
    return words

def tokenize_doc(doc):
    """

    Tokenize a document and return its bag-of-words representation.
    doc - a string representing a document.
    returns a dictionary mapping each word to the number of times it appears in doc.
    """
    bow = defaultdict(float)
    # lowered_tokens = map(lambda t: t.lower(), tokens)
    for lines in doc:
        tokens = lines.split()
        lowered_tokens = map(lambda t: t.lower(), tokens)
        for token in lowered_tokens:
            bow[token] += 1.0
    return bow

def get_lemma(word):
    lemma_n = lmtzr.lemmatize(word)
    lemma_v = lmtzr.lemmatize(word, 'v')
    if lemma_n == lemma_v:
        return lemma_n
    elif lemma_n is word and lemma_v is word:
        return word
    elif lemma_v is word and lemma_n is not word:
        return lemma_n
    return lemma_v

nb = NaiveBayes()
filenames = os.listdir(PATH_TO_TRAIN)
for f in filenames:
    print f
    lyrics = read_lyrics_from_file(os.path.join(PATH_TO_TRAIN,f))
    classification = lyrics.pop(0).rstrip().split(',')
    sentiment = classification.pop(0)
    words = tokenize_doc(lyrics)
    nb.update_model(words, sentiment)
nb.report_statistics_after_training()
    # for word in words:
    #     nb.class_total_word_counts[sentiment] += 1
    #     word = re.sub("[^a-zA-Z]+", "", word)
    #     word = word.lower()
    #     lemma = get_lemma(word)
    #     nb.class_word_counts[sentiment][lemma] += 1
    #     vocab.add(lemma)

# print nb.class_total_doc_counts
# print nb.top_n('-', 10)
