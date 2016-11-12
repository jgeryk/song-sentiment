from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
import re
import os

lmtzr = WordNetLemmatizer()
NEG_TAG = '-'
POS_TAG = '+'
NEU_TAG = '0'
PATH_TO_TRAIN = os.getcwd() + '/lyrics_annotated/test/'

def read_lyrics_from_file(file):
    words = []
    f = open(file)
    for line in f:
        words.append(line)
    return words

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

class NaiveBayes:
    def __init__(self):
        # Vocabulary is a set that stores every word seen in the training data
        self.vocab = set()
        # class_total_doc_counts is a dictionary that maps a class (i.e., pos/neg) to
        # the number of documents in the training set of that class
        self.class_total_doc_counts = { POS_TAG: 0.0,
                                        NEG_TAG: 0.0,
                                        NEU_TAG: 0.0 }

        # class_total_word_counts is a dictionary that maps a class (i.e., pos/neg) to
        # the number of words in the training set in documents of that class
        self.class_total_word_counts = { POS_TAG: 0.0,
                                         NEG_TAG: 0.0,
                                         NEU_TAG: 0.0 }

        # class_word_counts is a dictionary of dictionaries. It maps a class (i.e.,
        # pos/neg) to a dictionary of word counts. For example:
        #    self.class_word_counts[POS_LABEL]['awesome']
        # stores the number of times the word 'awesome' appears in documents
        # of the positive class in the training documents.
        self.class_word_counts = { POS_TAG: defaultdict(float),
                                   NEG_TAG: defaultdict(float),
                                   NEU_TAG: defaultdict(float) }
    def top_n(self, label, n):
        """

        Returns the most frequent n tokens for documents with class 'label'.
        """
        return sorted(self.class_word_counts[label].items(), key=lambda (w,c): -c)[:n]
        # def update_bow(lemmas, class):


nb = NaiveBayes()
filenames = os.listdir(PATH_TO_TRAIN)
for f in filenames:
    vocab = set()
    lyrics = read_lyrics_from_file(os.path.join(PATH_TO_TRAIN,f))
    classification = lyrics.pop(0).rstrip().split(',')
    sentiment = classification.pop(0)
    nb.class_total_doc_counts[sentiment] += 1
    for line in lyrics:
        words = line.split()
        for word in words:
            nb.class_total_word_counts[sentiment] += 1
            nb.class_word_counts[sentiment][word] += 1
            word = re.sub("[^a-zA-Z]+", "", word)
            word = word.lower()
            lemma = get_lemma(word)
            vocab.add(lemma)
# print nb.class_total_doc_counts
# print nb.top_n('-', 10)
