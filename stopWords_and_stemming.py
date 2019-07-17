import io 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

from nltk.stem import WordNetLemmatizer 
  
lemmatizer = WordNetLemmatizer() 

#word_tokenize accepts a string as an input, not a file. 
stop_words = set(stopwords.words('english')) 
i = 'I'
ok = 'ok'
stop_words.add(i)
stop_words.add(ok)

print(stop_words)
file1 = open("vk_clean.txt") 
line = file1.read()# Use this to read file content as a stream: 
words = line.split() 
for r in words: 
	if not r in stop_words:
         
		appendFile = open('vk_filtered.txt','a') 
		appendFile.write(lemmatizer.lemmatize(r)+" \n ") 
		appendFile.close() 

# >>> from textblob import TextBlob, Word
# >>> word = 'talking'
# >>> w.Word(word)
# >>> w = Word(word)
# >>> w.lemmatize()
# 'talking'
# >>> w.stem()
# 'talk'