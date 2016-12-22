from __future__ import division
import math
import pandas as pd
import heapq as heap
from util import *

class SimpleAveraging:
    # def __init__(self):
    #Calculates the angle of an x,y coordinate
    def __init__(self):
        self.sentiment_data = pd.read_csv('Ratings_Warriner_et_al.csv')
        self.thresholds = {
            POS_TAG: 2.25,

        }
        self.doc_counts = {
        POS_TAG : 103,
        NEG_TAG : 104,
        NEU_TAG : 91
        }
        self.avg_valence = {
        POS_TAG : 0.0,
        NEG_TAG : 0.0,
        NEU_TAG : 0.0
        }
        self.avg_arousal = {
        POS_TAG : 0.0,
        NEG_TAG : 0.0,
        NEU_TAG : 0.0
        }
        self.avg_valence_std_dev = {
        POS_TAG : 0.0,
        NEG_TAG : 0.0,
        NEU_TAG : 0.0
        }
        self.avg_arousal_std_dev = {
        POS_TAG : 0.0,
        NEG_TAG : 0.0,
        NEU_TAG : 0.0
        }
        self.unique_lemmas = set()
        self.unused_lemmas = set()
        self.lemma_count = 0.0
        self.correct_count = 0.0


    def calculate_angle(self, x, y):
        degrees = math.degrees(math.atan2(y, x))
        if degrees < 0:
            degrees = 360 - (-degrees)
        return degrees

    def get_stats(self, data):
        avgs = defaultdict(float)
        for f in data:
            lyrics = read_lyrics_from_file(os.path.join(PATH_TO_DATA,f))
            classification = lyrics.pop(0).rstrip().split(',')
            sentiment = classification.pop(0)
            lemmas = tokenize_doc_words(lyrics)
            classes = self.qualify(lemmas, 0, 0)
            # prediction = self.simple_classify(classes)
            # if sentiment == prediction:
            #     self.correct_count += 1
            self.avg_valence[sentiment] += classes['Valence']
            self.avg_valence_std_dev[sentiment] += classes['Std_Dev_Valence']
            self.avg_arousal[sentiment] += classes['Arousal']
            self.avg_arousal_std_dev[sentiment] += classes['Std_Dev_Arousal']
        print 'UNIQUE LEMMAS USED: ', len(self.unique_lemmas)
        # print 'UNUSED LEMMAS: ', self.unused_lemmas
        print 'LEMMA COUNT: ', self.lemma_count
        for sentiment in ['+', '0', '-']:
            avgs[sentiment + '_valence'] = self.avg_valence[sentiment] / self.doc_counts[sentiment]
            avgs['avg_' + sentiment + '_arousal'] = self.avg_arousal[sentiment] / self.doc_counts[sentiment]
            print sentiment, ' TAG AVG VALENCE: ', self.avg_valence[sentiment] / self.doc_counts[sentiment]
            print sentiment, ' TAG AVG STD DEV VALENCE: ', self.avg_valence_std_dev[sentiment] / self.doc_counts[sentiment]
            print sentiment, ' TAG AVG AROUSAL: ', self.avg_arousal[sentiment] / self.doc_counts[sentiment]
            print sentiment, ' TAG AVG STD DEV VALENCE: ', self.avg_valence_std_dev[sentiment] / self.doc_counts[sentiment]
        return avgs



    def train(self, training_set):
        return self.get_stats(training_set)

    def evaluate(self, test_set, avgs):
        self.sentiment_correct_count = 0
        self.affect_correct_count = 0
        avg_valence = (avgs['+_valence'] + avgs['0_valence'] + avgs['-_valence']) / 3
        std_dev = math.sqrt(sum([(avgs[sentiment + '_valence'] - avg_valence)*(avgs[sentiment + '_valence'] - avg_valence) for sentiment in ['+', '0', '-']]) / 3)
        print "STANDARD DEVIATION: ", std_dev
        # valence_deviation =  (avgs['+_valence'] - avgs['-_valence']) / 3
        valence_threshold_high = avgs['+_valence'] - std_dev
        valence_threshold_low = avgs['-_valence'] + std_dev
        print valence_threshold_high
        print valence_threshold_low
        for f in test_set:
            lyrics = read_lyrics_from_file(os.path.join(PATH_TO_DATA,f))
            classification = lyrics.pop(0).rstrip().split(',')
            sentiment = classification.pop(0)
            lemmas = tokenize_doc_words(lyrics)
            classes = self.qualify(lemmas, 0, 0)
            sentiment_prediction = self.simple_classify(classes, valence_threshold_high, valence_threshold_low)
            affect_prediction = self.classify(classes, -2.2, 1.7)
            if sentiment == sentiment_prediction:
                self.sentiment_correct_count += 1
            if str(affect_prediction) in classification:
                self.affect_correct_count += 1
        print 100*self.sentiment_correct_count / len(test_set)
        print 100*self.affect_correct_count / len(test_set)
        return (100*self.sentiment_correct_count / len(test_set), 100*self.affect_correct_count / len(test_set))


    def qualify(self, lyrics, valence_bias, arousal_bias):
        valence, arousal, std_dev_arousal, std_dev_valence = 0,0,0,0
        word_count = 0
        for word in lyrics:
            word_data = self.sentiment_data[self.sentiment_data['Word'] == word]
            if not word_data.empty:
                self.unique_lemmas.add(word)
                self.lemma_count += 1
                word_count += 1
                # print word, ' Arousal: ', 2.5*(float(word_data['A.Mean.Sum'])-5), '  Valence: ', 2.5*(float(word_data['V.Mean.Sum'])-5)
                arousal += (2.5*(float(word_data['A.Mean.Sum']) - 5)) + arousal_bias
                valence += (2.5*(float(word_data['V.Mean.Sum']) - 5)) + valence_bias
                std_dev_valence += float(word_data['V.SD.Sum'])
                std_dev_arousal += float(word_data['A.SD.Sum'])
            else:
                self.unused_lemmas.add(word)
        # print arousal/word_count
        # print valence/word_count
        return {'Valence': valence/word_count, 'Arousal': arousal/word_count, 'Std_Dev_Valence': (std_dev_valence)/(word_count), 'Std_Dev_Arousal': (std_dev_arousal)/(word_count), 'Lemmas': word_count}

    def simple_classify(self, lyric_stats, valence_threshold_high, valence_threshold_low):
        if lyric_stats['Valence'] > valence_threshold_high:
            return '+'
        elif lyric_stats['Valence'] < valence_threshold_low:
            return '-'
        return '0'


    def classify(self, lyric_stats, valence_bias, arousal_bias):
        angle_degrees = self.calculate_angle(lyric_stats['Valence'] + valence_bias, lyric_stats['Arousal'] + arousal_bias)
        emotion_degree = (math.ceil(angle_degrees / 30)) * 30
        return int(emotion_degree)

# lyrics = read_lyrics_from_file(SONG_FILE)
# qual = qualify(lyrics)
# classify(qual)
