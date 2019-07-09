from nltk import lm
from nltk.corpus import brown
from nltk.util import bigrams
from nltk.util import pad_sequence
from nltk.util import everygrams
from nltk.lm.preprocessing import pad_both_ends, flatten, padded_everygram_pipeline

from nltk.lm import MLE

#What we need
#1. a corpus (Training set and test set)
#2. Preprocessing

def main():
    #Preprocessing Phrase 

    #A very very small corpus with 2 sentences
    text = [['a', 'b', 'c'], ['a', 'c', 'd', 'c', 'e', 'f']]

    #Getting the first sentence
    first_text = text[0]

    #Perform padding to be able to find the most likely word beginning/ending a sentence
    padded_text = list(pad_both_ends(first_text, n=2)) # 2 for bigrams

    #Everygrams calculates unigram, bigram, trigram, . . ., ngram for us (max_len = 3 means from unigram to trigram)
    print(list(everygrams(padded_text, max_len=3)))

    #Flat the sentence array to array of words to make a vocabulary ()
    flattened = list(flatten(pad_both_ends(sent, n=3) for sent in text))
  
    print(flattened)
    train, vocab = padded_everygram_pipeline(3, text)
    print(train, vocab)

    #Training Phrase
    #Maximum Likelihood Estimation 
    # (Most probably that a particular word will have the probability = x in a given corpus found by using relative frequency)
    # 3 means maximum gram (trigram)
    lm = MLE(3) #MLE

    #First output = a blank vocabulary (will be filled when the model is trained)
    print("Our first empty vocabulary", len(lm.vocab))

    #Give the training data and our vocab to the library to train for us
    lm.fit(train, vocab)
    print("Our vocabulary after trained", lm.vocab)

    #Lets play with our model!

    #We can find word in the vocabulary (<UNK> means the word does not belong to the vocab!)
    print(lm.vocab.lookup(['a', 'b', 'c', 'x']))

    #Finding count in each gram. We have 3 ngram order and 45 ngrams (what does it mean by 45 ngrams?) 
    print(lm.counts)

    #Let's begin with counting a unigram
    print(lm.counts['a'])

    #Then bigram
    print(lm.counts[['a']]['b'])

    #Then trigram. . .
    print(lm.counts[['a','b']]['c'])

    #Relative Frequency (Joint probability)
    print(lm.score('a'))

    #Which word has the most score?
    print(lm.score('<s>'))

    total_score_unigram = 0
    print(flattened)

    #unigram score for w = P(w) = Count(w)/N
    print(lm.score('a'))
    print(lm.score('b'))

    #Avoiding underflow we use logprob
    print(lm.logscore('a'))
    print(lm.logscore('b'))


    #The score in the model for each gram must sum up to exactly 1
    bag_of_word = set(flattened)
    for word in bag_of_word:
        total_score_unigram += lm.score(word)

    print(total_score_unigram)
    total_score_bigram = 0

    #score for a word w given x = P(w | x) = C(w,x)/C(x)
    for word in bag_of_word:
        total_score_bigram += lm.score(word, ['a'])

    print(total_score_bigram)    

    #Generating a random sequence of words
    print(lm.generate(10)) 

    print(lm.generate(10, random_seed=3)) #Same random seed, the same sequence

    print(lm.generate(10, text_seed=['a'], random_seed=3)) #given 'a' as the preceding word)

    #Testing Phrase
    #Given a heldout corpus (additional corpus distinct to the traning corpus)
    test_seq = [('a', 'b'), ('c', 'd'), ('e', 'f')]
    test_good_seq =  list(bigrams(lm.vocab.lookup(['f', 'b', 'c', 'e'])))
    print(test_good_seq)
    #Evaluate by calculating entropy or perplexity of sequences of words
    print("Entropy: ", lm.entropy(test_seq), "Perplexity: ", lm.perplexity(test_seq))
    print("Entropy: ", lm.entropy(test_good_seq), "Perplexity: ", lm.perplexity(test_good_seq))

    #Homework
    #Why the value of entropy and perplexity sometimes is inf
    #How to avoid that?
        #Hint: Smoothing, backoff-interpolations
    
    #Try using different corpus and
    #Generate a random sentence in unigram, bigram and trigram and see

    def list_followers(self, word):
        followers = set()
        for tup in list(bigrams(flattened)):
            if tup[0]  == word:
                followers.add(tup[1])
        print(followers)
        return followers

if __name__ == "__main__":
    main()
