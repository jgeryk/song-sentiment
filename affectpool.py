from simpleaveraging import SimpleAveraging
from naivebayes import NaiveBayes
from collections import defaultdict


class AffectPool:
    def __init__(self, NaiveBayes, SimpleAveraging):
        self.nb = NaiveBayes
        self.sa = SimpleAveraging
        self.lemma_data = defaultdict(float)

    def simple_train(self, training_set):
        self.nb.train_model(training_set)
        avgs = self.sa.train(training_set)
        for lemma in ['hate']:
            lemma_data = self.sentiment_data[self.sentiment_data['Word'] == word]
            if not lemma_data.empty:
                lemma_data[lemma] = {'Valence': (2.5*(float(lemma_data['V.Mean.Sum']) - 5)), 'Arousal': (2.5*(float(word_data['A.Mean.Sum']) - 5))}
            sentiment_probs = self.nb.lemma_max_likelihoods_simple(lemma, 0.3)
            # affect_probs =
            print sentiment_probs
            print 'ay'


    def evaluate():
        pass
