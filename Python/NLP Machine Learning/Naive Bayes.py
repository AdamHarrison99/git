import nltk, random
nltk.download('movie_reviews')
nltk.download('punkt')

from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.probability import FreqDist

docs = []                                                    # Our custom dataset list
for label in movie_reviews.categories():                     # Categories are 'neg' and 'pos'
  files = movie_reviews.fileids(label)                       # Get list of file names associated with label
  for file in files:
    raw_words_from_file = movie_reviews.words(file)          # Get words in file (one movie review)
    word_set_with_features = FreqDist(raw_words_from_file)   # Use word counts as features
    words_with_label = (word_set_with_features, label)       # Put features together with label in a tuple
    docs.append(words_with_label)                            # Add tuple to our docs list

docs[:5]                                                     # Print a few docs to see formatting

#shuffle docs and split into sets
random.shuffle(docs)
docs_train = docs[:int(len(docs)/10*9)]
docs_test = docs[int(len(docs)/10*9):]
print("docs_train: ", len(docs_train), "\ndocs_test: ", len(docs_test))

train_classifier = NaiveBayesClassifier.train(docs_train)
print(train_classifier.labels())
print(train_classifier.most_informative_features(10))

#train and test our classifier
correct_cnt = 0
for review in docs_test:
    if train_classifier.classify(review[0]) == review[1]:
        correct_cnt += 1
print("Accuracy: %", (correct_cnt/len(docs_test))*100)
