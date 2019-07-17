
import nltk
from nltk import word_tokenize

str1 = "*CHI:"
str2 = "*ADU:"
mor = "%mor"
i=0
j=0
delete_list = ['?',',','.','_','@c','@o','@b']
with open("vk.txt") as file:

    with open("vk_adult_child_test.txt", "w") as f1:  
        with open("vk_adult_child_tokens.txt","w") as f2:       
            for line in file:

                #extracting only adu and chi lines and removing adu chi tags
                if str1 in line:
                    line = line.replace(str1, "")
                    f1.write(line)
                    i = i+1       
                    tokens_chi = nltk.word_tokenize(line)
                    f2.write(str(tokens_chi))

                elif str2 in line:
                    line = line.replace(str2, "")
                    f1.write(line)
                    j=j+1
                    tokens_adu = nltk.word_tokenize(line)
                    f2.write(str(tokens_adu))
            
        
                    



print("Child: "+str(i))
print("Adult: "+str(j))
print(len(tokens_chi))