import nltk
import random
nltk.download('vader_lexicon')
nltk.download('movie_reviews')
nltk.download('punkt')

from nltk.sentiment import vader
from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.probability import FreqDist

raw_docs = []                                     # Our custom dataset list
for label in movie_reviews.categories():          # Categories are 'neg' and 'pos'
  files = movie_reviews.fileids(label)            # Get list of file names associated with label
  for file in files:
    words_from_file = movie_reviews.words(file)   # Get words in file (one movie review)
    words_with_label = (words_from_file, label)   # Place raw words with label in a tuple
    raw_docs.append(words_with_label)             # Add tuple to our docs list

random.shuffle(raw_docs)                          # Randomize document positions
raw_docs[:5]

#FreqDist label and unigram count list
docs = []
for doc in raw_docs:
    word_set_with_features = FreqDist(doc[0])
    words_with_label = (word_set_with_features, doc[1])
    docs.append(words_with_label)

docs[:5]

#Create and test lexicon.
lexicon = vader.SentimentIntensityAnalyzer().make_lex_dict() # Get lexicon

print("happy:", lexicon['happy'])        # Very positive
print("terrible:", lexicon['terrible'])  # Very negative
print("okay:", lexicon['okay'])          # Fairly neutral

#Find teh sentiment of each token
sentiment_docs = []
lexicon_dict = {}
for doc in raw_docs:
    for word in doc[0]:
        if word in lexicon and word not in lexicon_dict:
            lexicon_dict[word] = lexicon[word]
    lexicon_with_label = (lexicon_dict, doc[1])
    sentiment_docs.append(lexicon_with_label)
    lexicon_dict = {}

sentiment_docs[:1]

#function for splitting set into train and test
def split_train_and_test(dataset = [], training_set_ratio = 0.9):
    if training_set_ratio == 1.0: # all for training
        train_set = dataset
        test_set = []
    else:
        train_set = dataset[:int(len(docs)/100*(training_set_ratio))]
        test_set = dataset[int(len(docs)/100*training_set_ratio):]

    return (train_set, test_set)

#Train, test, and print results
docs_train_test = split_train_and_test(docs)
sentiment_train_test = split_train_and_test(sentiment_docs)

docs_classifier = NaiveBayesClassifier.train(docs_train_test[0])
sentiment_classifier = NaiveBayesClassifier.train(sentiment_train_test[0])

print("docs_classifier: ", docs_classifier.most_informative_features(10), "\n\n",
      "sentiment_classifier: ", sentiment_classifier.most_informative_features(10))

#Classifying features and comparing the prediction with the reality
def confusion_matrix(classifier, test_set = []):
    TP = 0; FP = 0; TN = 0; FN = 0
    for doc in test_set: #should prob use swich statement but lazy
        if classifier.classify(doc[0]) == "pos" and doc[1] == "pos":
            TP += 1
        elif classifier.classify(doc[0]) == "pos" and doc[1] == "neg":
            FP += 1
        elif classifier.classify(doc[0]) == "neg" and doc[1] == "neg":
            TN += 1
        elif classifier.classify(doc[0]) == "neg" and doc[1] == "pos":
            FN += 1

    return (TP, FP, TN, FN)

#f1 score, used to measure classifier affectiveness
def f1_score(classifier, test_set = []):
    results = confusion_matrix(classifier, test_set)
    precision = results[0]/results[0]+results[1]
    recall = results[0]/results[0]+results[3]
    f1 = 2*(precision*recall)/precision+recall

    return f1

print("docs f1: ", f1_score(docs_classifier, docs_train_test[1]), "\n\n",
     "sentiment f1: ", f1_score(sentiment_classifier, sentiment_train_test[1]))
