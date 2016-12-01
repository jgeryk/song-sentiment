from collections import defaultdict

NEG_TAG = '-'
POS_TAG = '+'
NEU_TAG = '0'

class NaiveBayes:
    def __init__(self):
        # Vocabulary is a set that stores every word seen in the training data
        self.vocab = set()
        self.affect_tag_count = 0.0
        self.total_affect_counts = defaultdict(float)
        # class_total_doc_counts is a dictionary that maps a class (i.e., pos/neg) to
        # the number of documents in the training set of that class
        self.class_total_doc_counts = { POS_TAG: 0.0,
                                        NEG_TAG: 0.0,
                                        NEU_TAG: 0.0 }

        # class_total_word_counts is a dictionary that maps a class (i.e., pos/neg) to
        # the number of words in the training set in documents of that class
        self.class_total_word_counts = { POS_TAG: 0.0,
                                         NEG_TAG: 0.0,
                                         NEU_TAG: 0.0 }

        # class_word_counts is a dictionary of dictionaries. It maps a class (i.e.,
        # pos/neg) to a dictionary of word counts. For example:
        #    self.class_word_counts[POS_LABEL]['awesome']
        # stores the number of times the word 'awesome' appears in documents
        # of the positive class in the training documents.
        self.class_word_counts = { POS_TAG: defaultdict(float),
                                   NEG_TAG: defaultdict(float),
                                   NEU_TAG: defaultdict(float) }

    def update_model(self, bow, label):
        self.class_total_doc_counts[label] += 1.0
        for token in bow:
            self.class_total_word_counts[label] += bow[token]
            self.class_word_counts[label][token] += bow[token]
            self.vocab.add(token)

    def report_statistics_after_training(self):
        """
        Report a number of statistics after training.
        """
        print "REPORTING CORPUS STATISTICS"
        print "NUMBER OF DOCUMENTS IN POSITIVE CLASS:", self.class_total_doc_counts[POS_TAG]
        print "NUMBER OF DOCUMENTS IN NEUTRAL CLASS:", self.class_total_doc_counts[NEU_TAG]
        print "NUMBER OF DOCUMENTS IN NEGATIVE CLASS:", self.class_total_doc_counts[NEG_TAG]
        print "NUMBER OF TOKENS IN POSITIVE CLASS:", self.class_total_word_counts[POS_TAG]
        print "NUMBER OF TOKENS IN NEUTRAL CLASS:", self.class_total_word_counts[NEU_TAG]
        print "NUMBER OF TOKENS IN NEGATIVE CLASS:", self.class_total_word_counts[NEG_TAG]
        print "AVERAGE AFFECT TAGS PER SONG:", self.affect_tag_count/sum(class_total_doc_counts.values())
        print "VOCABULARY SIZE: NUMBER OF UNIQUE WORDTYPES IN TRAINING CORPUS:", len(self.vocab)

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
        posLog = self.unnormalized_log_posterior(bow, POS_LABEL, alpha)
        neuLog = self.unnormalized_log_posterior(bow, POS_LABEL, alpha)
        negLog = self.unnormalized_log_posterior(bow, NEG_LABEL, alpha)
        return POS_LABEL if posLog > negLog else NEG_LABEL
