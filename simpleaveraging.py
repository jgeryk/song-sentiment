from __future__ import division
import math
import pandas as pd
import heapq as heap

data = pd.read_csv('Ratings_Warriner_et_al.csv')
SONG_FILE = 'lyrics/of_montreal/spiteful_intervention.txt'

affect_map = {
    30: 'Happy',
    60: 'Excited',
    90: 'Alert',
    120: 'Tense',
    150: 'Stressed',
    180: 'Upset',
    210: 'Sad',
    240: 'Depressed',
    270: 'Bored',
    300: 'Calm',
    330: 'Serene',
    360: 'Content'
}

class SimpleAveraging:
    # def __init__(self):
    #Calculates the angle of an x,y coordinate
    def calculate_angle(self, x, y):
        degrees = math.degrees(math.atan2(y, x))
        if degrees < 0:
            degrees = 360 - (-degrees)
        return degrees

    def qualify(self, lyrics, valence_bias, arousal_bias):
        valence, arousal, std_dev_arousal, std_dev_valence = 0,0,0,0
        word_count = 0
        for word in lyrics:
            word_data = data[data['Word'] == word]
            if not word_data.empty:
                word_count += 1
                # print word, ' Arousal: ', 2.5*(float(word_data['A.Mean.Sum'])-5), '  Valence: ', 2.5*(float(word_data['V.Mean.Sum'])-5)
                arousal += (2.5*(float(word_data['A.Mean.Sum']) - 5)) + arousal_bias
                valence += (2.5*(float(word_data['V.Mean.Sum']) - 5)) + valence_bias
                std_dev_valence += float(word_data['V.SD.Sum'])
                std_dev_arousal += float(word_data['A.SD.Sum'])
        # print arousal/word_count
        # print valence/word_count
        return {'Valence': valence, 'Arousal': arousal, 'Std_Dev': (std_dev_valence+std_dev_arousal)/(word_count*2)}

    def simple_classify(self, lyric_stats):
        if lyric_stats['Valence'] > 3:
            return '+'
        elif lyric_stats['Valence'] < -3:
            return '-'
        return '0'


    def classify(self, lyric_stats):
        angle_degrees = self.calculate_angle(lyric_stats['Valence'], lyric_stats['Arousal'])
        emotion_degree = (math.ceil(angle_degrees / 30)) * 30
        return emotion_degree

# lyrics = read_lyrics_from_file(SONG_FILE)
# qual = qualify(lyrics)
# classify(qual)
