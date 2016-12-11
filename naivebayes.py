from collections import defaultdict
import os, math
from util import *
import heapq as heap

class NaiveBayes:
    def __init__(self):
        # Vocabulary is a set that stores every word seen in the training data
        self.vocab = set()
        self.affect_tag_count = 0.0
        self.total_affect_counts = defaultdict(float)
        # class_total_doc_counts is a dictionary that maps a class (i.e., pos/neg) to
        # the number of documents in the training set of that class
        self.class_total_doc_counts = defaultdict(float)

        # class_total_word_counts is a dictionary that maps a class (i.e., pos/neg) to
        # the number of words in the training set in documents of that class
        self.class_total_word_counts = defaultdict(float)

        # class_word_counts is a dictionary of dictionaries. It maps a class (i.e.,
        # pos/neg) to a dictionary of word counts. For example:
        #    self.class_word_counts[POS_LABEL]['awesome']
        # stores the number of times the word 'awesome' appears in documents
        # of the positive class in the training documents.
        self.class_word_counts = defaultdict(lambda : defaultdict(float))

    def train_model(self, training_set):
        for f in training_set:
            lyrics = read_lyrics_from_file(os.path.join(PATH_TO_DATA,f))
            classification = lyrics.pop(0).rstrip().split(',')
            sentiment = classification.pop(0)
            lemmas_as_bow = tokenize_doc_bow(lyrics)
            self.update_model(lemmas_as_bow, sentiment, classification)
        self.report_statistics_after_training()
        self.report_most_likely_words(self.class_word_counts['+'])

    def update_model(self, bow, label, sentiments):
        self.class_total_doc_counts[label] += 1.0
        for s in sentiments:
            self.class_total_doc_counts[s] += 1.0
        for token in bow:
            self.class_total_word_counts[label] += bow[token]
            self.class_word_counts[label][token] += bow[token]
            self.vocab.add(token)
            for s in sentiments:
                self.class_total_word_counts[s] += bow[token]
                self.class_word_counts[s][token] += bow[token]

    def report_most_likely_words(self, label):
        likelihoods = defaultdict(float)
        for word in words:
            heap.



    def p_word_given_label_and_psuedocount(self, word, label, alpha):
        return (self.class_word_counts[label][word] + alpha) / (self.class_total_word_counts[label] + alpha)

    def likelihood_ratio(self, word, alpha):
        return self.p_word_given_label_and_psuedocount(word, POS_LABEL, alpha) / self.p_word_given_label_and_psuedocount(word, NEG_LABEL, alpha)

    def report_statistics_after_training(self):
        print self.top_n('+', 10)
        # for c in self.class_total_doc_counts.keys():
        #     print "NUMBER OF DOCUMENTS IN ", c, " CLASS: ", self.class_total_doc_counts[c]
            # print "NUMBER OF LEMMAS IN ", c, " CLASS: ", self.class_total_word_counts[c]
        # """
        # Report a number of statistics after training.
        # """
        # print "REPORTING CORPUS STATISTICS"
        # print "NUMBER OF DOCUMENTS IN POSITIVE CLASS:", self.class_total_doc_counts[POS_TAG]
        # print "NUMBER OF DOCUMENTS IN NEUTRAL CLASS:", self.class_total_doc_counts[NEU_TAG]
        # print "NUMBER OF DOCUMENTS IN NEGATIVE CLASS:", self.class_total_doc_counts[NEG_TAG]
        # print "NUMBER OF TOKENS IN POSITIVE CLASS:", self.class_total_word_counts[POS_TAG]
        # print "NUMBER OF TOKENS IN NEUTRAL CLASS:", self.class_total_word_counts[NEU_TAG]
        # print "NUMBER OF TOKENS IN NEGATIVE CLASS:", self.class_total_word_counts[NEG_TAG]
        # print "VOCABULARY SIZE: NUMBER OF UNIQUE WORDTYPES IN TRAINING CORPUS:", len(self.vocab)

    def evaluate_model(self, test_set):
        sentiment_correct_count = 0.0
        emotions_count = 0.0
        correct_emotions_count = 0.0
        for f in test_set:
            lyrics = read_lyrics_from_file(os.path.join(PATH_TO_DATA,f))
            classification = lyrics.pop(0).rstrip().split(',')
            sentiment = classification.pop(0)
            lemmas_as_bow = tokenize_doc_bow(lyrics)
            predicted_sentiment, classifications = self.classify(lemmas_as_bow, 1)
            emotions_count += len(classification)
            if predicted_sentiment == sentiment:
                sentiment_correct_count += 1
            # top_classes = classifications.keys()
            sorted(classifications, key=classifications.get)
            classification_probs = classifications.keys()
            for top_class in classification_probs[:len(classification)]:
                if classifications[top_class] in classification:
                    correct_emotions_count += 1
        return (100*sentiment_correct_count/len(test_set), 100*correct_emotions_count/emotions_count)

    def top_n(self, label, n):
        """

        Returns the most frequent n tokens for documents with class 'label'.
        """
        return sorted(self.class_word_counts[label].items(), key=lambda (w,c): -c)[:n]
        # def update_bow(lemmas, class):

    def p_word_given_label(self, word, label):
        return self.class_word_counts[label][word] / self.class_total_word_counts[label]

    def p_word_given_label_and_psuedocount(self, word, label, alpha):
        return (self.class_word_counts[label][word] + alpha) / (self.class_total_word_counts[label] + alpha)

    def log_likelihood(self, bow, label, alpha):
        likelihood = 0;
        for word in bow:
            likelihood += math.log(self.p_word_given_label_and_psuedocount(word, label, alpha))
        return likelihood

    def log_prior(self, label):
        return math.log(self.class_total_doc_counts[label] / (sum(self.class_total_doc_counts.itervalues())))

    def unnormalized_log_posterior(self, bow, label, alpha):
        return self.log_likelihood(bow, label, alpha) + self.log_prior(label)

    def classify(self, bow, alpha):
        sentiment_probs = defaultdict(float)
        emotion_probs = defaultdict(float)
        for sentiment in ['+', '0', '-']:
            sentiment_probs[self.unnormalized_log_posterior(bow, sentiment, alpha)] = sentiment
        for label in self.class_total_doc_counts.keys():
            if label not in ['+', '0', '-']:
                emotion_probs[self.unnormalized_log_posterior(bow, label, alpha)] = label
        return (sentiment_probs[max(sentiment_probs.keys())], emotion_probs)
