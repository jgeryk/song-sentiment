from __future__ import division
from collections import defaultdict
import re
import os
import matplotlib.pyplot as plt
import sys
from random import sample
from util import *

from simpleaveraging import SimpleAveraging
from naivebayes import NaiveBayes
reload(sys)
sys.setdefaultencoding('utf8')


PATH_TO_TRAIN = os.getcwd() + '/song-sentiment-data'
PATH_TO_TEST = os.getcwd() + '/song-sentiment-data/test'


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


def cross_validate(folds, method):
    if folds < 2:
        print 'Must have at least 2 folds.. evaluating 2-fold cross validation'
        folds = 2
    test_size = 100/folds
    training_size = 100 - test_size
    songs_by_class = split_by_class()
    sentiment_accuracy_sum = 0.0
    emotion_accuracy_sum = 0.0
    for f in range(0,folds):
        test_set = songs_by_class['+'][int(test_size*f):int(test_size+test_size*f)] + songs_by_class['0'][int(test_size*f):int(test_size+test_size*f)] +songs_by_class['-'][int(test_size*f):int(test_size+test_size*f)]
        training_set = songs_by_class['+'][int(test_size+test_size*f):] + songs_by_class['+'][:int(test_size*f)] + songs_by_class['0'][int(test_size+test_size*f):] + songs_by_class['0'][:int(test_size*f)] + songs_by_class['-'][int(test_size+test_size*f):] + songs_by_class['-'][:int(test_size*f)]
        if method == 'nb':
            nb = NaiveBayes()
            nb.train_model(training_set)
            emotion_accuracy, sentiment_accuracy = nb.evaluate_model(test_set)
            emotion_accuracy_sum += emotion_accuracy
            sentiment_accuracy_sum += sentiment_accuracy
        elif method == 'sa':
            sa = SimpleAveraging()
            sa.get_stats(test_set + training_set)
            # sa.train(sample(training_set, len(training_set)))
        elif method =='r':
            nb = NaiveBayes()
            nb.train_model(test_set + training_set)
    # print "EMOTION ACCURACY ", emotion_accuracy_sum / folds, " SENTIMENT ACCURACY: ", sentiment_accuracy_sum / folds


def evaluate_sa_with_biases():
    training_set = os.listdir(PATH_TO_DATA)
    sa = SimpleAveraging()
    doc_count = 0.0
    sa_simple_accurate = 0.0
    sa_accurate = 0.0
    biases = []
    accuracies_simple = []
    accuracies = []
    for bias in drange(-1, 3.5, 0.5):
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

# report_statistics()
cross_validate(2, 'r')

# evaluate_sa_with_biases()
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
