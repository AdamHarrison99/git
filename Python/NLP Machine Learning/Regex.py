import nltk, re
from nltk.corpus import brown as nltkB
from nltk.corpus import twitter_samples
nltk.download('brown')
nltk.download('twitter_samples')

#Find total words(tokens) in corpus, and unique words, using regex
print("Total tokens:", len(nltkB.words()))

#List unique tokens in corpus, to lower
unique_tokens = set(nltkB.words())
print("Unique tokens:", len(unique_tokens))

unique_tokens_lower = [uLow.lower() for uLow in unique_tokens]

#print last 10, then sort and print
print("Last 10 tokens:", unique_tokens_lower[-10:])
print("Last 10 tokens sorted:", sorted(unique_tokens_lower)[-10:])

#find cat, cow using regex
pattern = re.compile(r'cat|cow')
text = "I love how cats meow and cows moo. I could be a cow in another life."
pattern.findall(text)

m = pattern.match("cat") # Do NOT use match as a variable name
m.group()

#print unique tokens
y_pattern = re.compile(r'[y]+[a-zA-Z0-9._-]+')
string = ' '.join([str(elem) for elem in unique_tokens_lower])

#print(y_pattern.findall(string))

#find and print all non alphanumeric characters
punc_pattern = re.compile(r'[^a-zA-Z0-9]+')
#print(punc_pattern.findall(string))

#print first 30 tweets in twitter corpus
print("Number of tweets:",len(twitter_samples.tokenized()))

print("First 30 tweets:", twitter_samples.strings()[:30])

#Produces users handles
#Also produces handles within the tweets themselvs
for tweet in twitter_samples.strings()[:30]:
    print(nltk.regexp_tokenize(tweet, "@+[A-Za-z0-9]+"))

#Create regex for addresses 
addresses = {
  "University of Denver": "2199 S University Blvd, Denver, CO 80208",
  "La Chiva Colombian Restaurant": "1446 S Broadway, Denver, CO 80210",
  "Red Rocks Amphitheatre": "18300 W Alameda Pkwy, Morrison, CO 80465",
  "16th Street Mall": "1001 16th St Mall, Denver, CO 80265",
  "Telluride Ski Resort": "565 Mountain Village Blvd, Telluride, CO 81435"
}

address_pattern = re.compile(r'(\d{1,5}) ([A-Za-z\s]+,) ([A-Za-z]+,) ([A-Z]{2}) ([0-9]{5})')
for address in addresses.values():
    match = address_pattern.match(address)
    if match != None:
        print(match.group())
