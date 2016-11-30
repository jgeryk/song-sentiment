from __future__ import division
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
import re
import os
import matplotlib.pyplot as plt
from simpleaveraging import SimpleAveraging
from naivebayes import NaiveBayes

lmtzr = WordNetLemmatizer()
NEG_TAG = '-'
POS_TAG = '+'
NEU_TAG = '0'
PATH_TO_DATA = os.getcwd() + '/song-sentiment-data'
PATH_TO_TRAIN = os.getcwd() + '/song-sentiment-data'
PATH_TO_TEST = os.getcwd() + '/song-sentiment-data/test'
vocab = set()
affect_tag_count = 0.0
total_affect_counts = defaultdict(float)
class_total_doc_counts = { POS_TAG: 0.0,
                                NEG_TAG: 0.0,
                                NEU_TAG: 0.0 }
class_total_word_counts = { POS_TAG: 0.0,
                                 NEG_TAG: 0.0,
                                 NEU_TAG: 0.0 }
class_word_counts = { POS_TAG: defaultdict(float),
                           NEG_TAG: defaultdict(float),
                           NEU_TAG: defaultdict(float) }

def read_lyrics_from_file(file):
    words = []
    f = open(file)
    for line in f:
        words.append(line)
    return words

def tokenize_doc_words(doc):
    """

    Tokenize a document and return its bag-of-words representation.
    doc - a string representing a document.
    returns a dictionary mapping each word to the number of times it appears in doc.
    """
    lemmas = []
    # lowered_tokens = map(lambda t: t.lower(), tokens)
    for lines in doc:
        tokens = lines.split()
        lowered_tokens = map(lambda t: t.lower(), tokens)
        for token in lowered_tokens:
            token = get_lemma(token)
            lemmas.append(token)
    return lemmas

def tokenize_doc_bow(doc):
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
            token = get_lemma(token)
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

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def split_by_class():
    pos_songs = []
    neu_songs = []
    neg_songs = []
    for f in os.listdir(PATH_TO_DATA):
        f = os.path.join(PATH_TO_TRAIN,f)
        with open(f, 'r') as txt:
            category = txt.readline().split(',')[0]
        if category == '+': pos_songs.append(f)
        elif category == '0': neu_songs.append(f)
        else: neg_songs.append(f)
    return {'+': pos_songs, '0': neu_songs, '-': neg_songs}

def reportStatistics():

def cross_validate(folds, method):
    test_size = 100/folds
    training_size = 100 - test_size
    songs_by_class = split_by_class()
    for f in range(0,folds):
        test_set = songs_by_class['+'][int(test_size*f):int(test_size+test_size*f)] + songs_by_class['0'][int(test_size*f):int(test_size+test_size*f)] +songs_by_class['-'][int(test_size*f):int(test_size+test_size*f)]
        training_set = songs_by_class['+'][int(test_size+test_size*f):] + songs_by_class['+'][:int(test_size*f)] + songs_by_class['0'][int(test_size+test_size*f):] + songs_by_class['0'][:int(test_size*f)] + songs_by_class['-'][int(test_size+test_size*f):] + songs_by_class['-'][:int(test_size*f)]
        if method == 'nb':


def evaluate_sa_with_biases():
    training_set = os.listdir(PATH_TO_TRAIN)
    sa = SimpleAveraging()
    doc_count = 0.0
    sa_simple_accurate = 0.0
    sa_accurate = 0.0
    biases = []
    accuracies_simple = []
    accuracies = []
    for bias in drange(-2.5, 3.5, 0.25):
        print bias
        biases.append(bias)
        for f in training_set:
            doc_count += 1.0
            lyrics = read_lyrics_from_file(os.path.join(PATH_TO_TRAIN,f))
            classification = lyrics.pop(0).rstrip().split(',')
            sentiment = classification.pop(0)
            lemmas_as_list = tokenize_doc_words(lyrics)
            lyrics_affect_data = sa.qualify(lemmas_as_list, -1.75, bias)
            # sent_pred = sa.simple_classify(lyrics_affect_data)
            emotion_pred = sa.classify(lyrics_affect_data)
            # print 'prediction: ', sent_pred, ' actual: ', sentiment
            # if sent_pred == sentiment:
            #     sa_simple_accurate += 1.0
            if str(int(emotion_pred)) in classification:
                sa_accurate += 1.0
        accuracies_simple.append(sa_simple_accurate/doc_count)
        accuracies.append(sa_accurate/doc_count)
        doc_count = 0.0
        sa_simple_accurate = 0.0
        sa_accurate = 0.0
    # plt.plot(biases, accuracies_simple)
    # plt.xlabel('Arousal bias')
    # plt.ylabel('Accuracy (%)')
    # plt.title('Simple Averaging: Valence Biases')
    # plt.show()
    plt.plot(biases, accuracies)
    plt.xlabel('Arousal Bias')
    plt.ylabel('Accuracy (%)')
    plt.title('Simple Averaging: Arousal Biases With Affect Map')
    plt.show()


# evaluate_sa_with_biases()
cross_validate(10, 'naive_bayes')
# nb = NaiveBayes()
# training_set = os.listdir(PATH_TO_TRAIN)
# doc_count = 0
# for f in training_set:
#     doc_count += 1.0
#     lyrics = read_lyrics_from_file(os.path.join(PATH_TO_TRAIN,f))
#     classification = lyrics.pop(0).rstrip().split(',')
#     sentiment = classification.pop(0)
#     lemmas_as_bow = tokenize_doc_bow(lyrics)
#     nb.update_model(lemmas_as_bow, sentiment)

    # lemmas_as_list = tokenize_doc_words(lyrics)
    # lyrics_affect_data = sa.qualify(lemmas_as_list, -2, 1)
    # sent_pred = sa.simple_classify(lyrics_affect_data)
    # if sent_pred == sentiment:
    #     sa_accurate += 1.0

# nb.report_statistics_after_training()
# print 'Doc Count ', doc_count
# print 'Correct ', sa_accurate, ': ', 100*sa_accurate/doc_count, '%'

# print nb.class_total_doc_counts
# print nb.top_n('-', 10)
