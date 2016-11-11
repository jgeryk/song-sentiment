from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()

def read_lyrics_from_file(file):
    words = []
    f = open(file)
    for lines in f.read():
        words.append(word)
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
