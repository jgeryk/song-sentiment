from collections import defaultdict
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()

import os
NEG_TAG = '-'
POS_TAG = '+'
NEU_TAG = '0'
PATH_TO_DATA = os.getcwd() + '/song-sentiment-data'
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


def read_lyrics_from_file(file):
    words = []
    f = open(file)
    for line in f:
        words.append(line)
    return words

def tokenize_doc_words(doc):
    lemmas = []
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

def report_statistics():
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
    for f in os.listdir(PATH_TO_DATA):
        f = os.path.join(PATH_TO_TRAIN,f)
        with open(f, 'r') as txt:
            lyrics = read_lyrics_from_file(os.path.join(PATH_TO_TRAIN,f))
            classification = lyrics.pop(0).rstrip().split(',')
            sentiment = classification.pop(0)
            lemmas_as_bow = tokenize_doc_bow(lyrics)
            class_total_doc_counts[sentiment] += 1.0
            for c in classification:
                affect_tag_count += 1.0
                total_affect_counts[c] += 1.0
            for lemma, count in lemmas_as_bow.iteritems():
                vocab.add(lemma)
                class_total_word_counts[sentiment] += count
                class_word_counts[sentiment][lemma] += count
    sorted(self.class_word_counts[label].items(), key=lambda (w,c): -c)[:n]
    print "REPORTING CORPUS STATISTICS"
    print "NUMBER OF DOCUMENTS IN POSITIVE CLASS:", class_total_doc_counts[POS_TAG]
    print "NUMBER OF DOCUMENTS IN NEUTRAL CLASS:", class_total_doc_counts[NEU_TAG]
    print "NUMBER OF DOCUMENTS IN NEGATIVE CLASS:", class_total_doc_counts[NEG_TAG]
    print "NUMBER OF LEMMAS IN POSITIVE CLASS:", class_total_word_counts[POS_TAG]
    print "NUMBER OF LEMMAS IN NEUTRAL CLASS:", class_total_word_counts[NEU_TAG]
    print "NUMBER OF LEMMAS IN NEGATIVE CLASS:", class_total_word_counts[NEG_TAG]
    print "AVERAGE AFFECT TAGS PER SONG:", affect_tag_count/sum(class_total_doc_counts.values())
    print total_affect_counts
    print "VOCABULARY SIZE: NUMBER OF UNIQUE LEMMAS IN TRAINING CORPUS:", len(vocab)
