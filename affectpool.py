from simpleaveraging import SimpleAveraging
from naivebayes import NaiveBayes
from collections import defaultdict


class AffectPool:
    def __init__(self, NaiveBayes, SimpleAveraging):
        self.nb = NaiveBayes
        self.sa = SimpleAveraging
        self.lemma_data = defaultdict(lambda : defaultdict(float))

    def simple_train(self, training_set):
        self.nb.train_model(training_set)
        # avgs = self.sa.train(training_set)
        for lemma in ['pain', 'happy', 'sunshine', 'sleep']:
            lemma_affects = self.sa.sentiment_data[self.sa.sentiment_data['Word'] == lemma]
            if not lemma_affects.empty:
                self.lemma_data[lemma]['Valence'] = 2.5*(float(lemma_affects['V.Mean.Sum']) - 5)
                self.lemma_data[lemma]['Arousal'] = 2.5*(float(lemma_affects['A.Mean.Sum']) - 5)
            sentiment_probs = self.nb.lemma_max_likelihoods_simple(lemma, 0.3, len(training_set))
            affect_probs = self.nb.lemma_max_likelihoods_affect(lemma, 0.3, len(training_set))
            # most_likely_ = max(stats, key=stats.get)
            # affect_probs =
            print lemma
            # print sentiment_probs
            print sentiment_probs[max(sentiment_probs.keys())]
            # print affect_probs
            print affect_probs[max(affect_probs.keys())]


    def evaluate():
        pass
