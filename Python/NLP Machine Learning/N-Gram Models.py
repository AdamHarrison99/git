import nltk
nltk.download('brown')
from nltk.corpus import brown as nltkB
from nltk.probability import FreqDist
from nltk.util import bigrams
from nltk.lm.preprocessing import pad_both_ends

#Frequency distribution of all unigrams, lower, print most common
my_freq_dist = FreqDist()
for i in nltkB.words():
    my_freq_dist[i.lower()] += 1

print("Most common tokens: ", my_freq_dist.most_common(10), end="\n\n")

#Another FreqDist, padded at both ends, lower, most common
my_freq_dist = FreqDist()
bigram_sentences = []

for i in nltkB.sents():
    i_low = [j.lower() for j in i]
    bigram_sentences += list(bigrams(pad_both_ends(i_low, 2)))

for j in bigram_sentences:
     my_freq_dist[j] += 1

print("Most common start and end:", my_freq_dist.most_common(10), end="\n\n")

#Most likely words to folow "the"
my_the_freq_dist = FreqDist()
for i in bigram_sentences:
    if i[0] == 'the':
        my_the_freq_dist[i[1]] += 1
print("The:", my_the_freq_dist.most_common(10))
