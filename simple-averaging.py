from __future__ import division
import math
import pandas as pd
import heapq as heap

data = pd.read_csv('Ratings_Warriner_et_al.csv')
SONG_FILE = 'lyrics/of_montreal/wintered_debts.txt'

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
    330: 'Serene'
}

def read_lyrics_from_file(file):
    words = []
    f = open(file)
    for word in f.read().split():
        words.append(word)
    return words
#Calculates the angle of an x,y coordinate
def calculate_angle(x, y):
    degrees = math.degrees(math.atan2(y, x))
    if degrees < 0:
        degrees = 360 - (-degrees)
    return degrees

# Index a word like this data[data['Word'] == 'aardvark']
def qualify(lyrics):
    valence, arousal, std_dev_arousal, std_dev_valence = 0,0,0,0
    word_count = 0
    for word in lyrics:
        word_data = data[data['Word'] == word]
        if not word_data.empty:
            word_count += 1
            print word, ' Arousal: ', float(word_data['A.Mean.Sum']), '  Valence: ', float(word_data['V.Mean.Sum'])
            arousal += 2.5*(float(word_data['A.Mean.Sum'])-5)
            valence += 2.5*(float(word_data['V.Mean.Sum'])- 5)
            std_dev_valence += float(word_data['V.SD.Sum'])
            std_dev_arousal += float(word_data['A.SD.Sum'])
    # avg_valence_scaled = ((valence/word_count)-5) * 2.5
    # avg_arousal_scaled = ((arousal/word_count)-5) * 2.5
    print arousal/word_count
    print valence/word_count
    return {'Valence': valence, 'Arousal': arousal, 'Std_Dev': (std_dev_valence+std_dev_arousal)/(word_count*2)}

def classify(lyric_stats):
    angle_degrees = calculate_angle(lyric_stats['Valence'], lyric_stats['Arousal'])
    emotion_degree = (math.ceil(angle_degrees / 30)) * 30
    print affect_map[emotion_degree]

lyrics = read_lyrics_from_file(SONG_FILE)
qual = qualify(lyrics)
classify(qual)
