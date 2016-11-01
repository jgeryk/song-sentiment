import pandas as pd
data = pd.read_csv('Ratings_Warriner_et_al.csv')

# Index a word like this data[data['Word'] == 'aardvark']
def classify(lyrics):
    avg_valence = 0
    avg_arousal = 0
    for word in lyrics:
    pass
