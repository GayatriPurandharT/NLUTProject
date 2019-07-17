import io 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

from nltk.stem import WordNetLemmatizer 
  
lemmatizer = WordNetLemmatizer() 

#word_tokenize accepts a string as an input, not a file. 
stop_words = set(stopwords.words('english')) 
insert = { 'I' , 'ok', 'okay', ',', 'yeah', 'u', ' u ', 'put', 'go', 'ow' }
# ok = 'ok'
for i in insert:
	stop_words.add(i)
# stop_words.add(ok)

# print(stop_words)
# file1 = open("vankleekcorpus.vert") 
# line = file1.read()# Use this to read file content as a stream: 
# words = line.split() 

with open("lex.txt") as file:
    for line in file:
        words = line.split()
        # print(words) 
        if words[0] not in stop_words:
            appendFile = open('lexicon.txt','a') 
            appendFile.write(line) 
            appendFile.close() 

# >>> from textblob import TextBlob, Word
# >>> word = 'talking'
# >>> w.Word(word)
# >>> w = Word(word)
# >>> w.lemmatize()
# 'talking'
# >>> w.stem()
# 'talk'