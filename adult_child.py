str1 = "*CHI"
str2 = "*ADU"
mor = "%mor"
i=0
j=0
with open("vk.txt") as file:
    with open("vk_adult.txt", "w") as f1:
        with open("vk_child.txt", "w") as f2:         
            for line in file:
                if str1 in line:
                    f1.write(line)
                elif mor in line:
                                    
                elif str2 in line:
                    j=j+1
                    f2.write(line)
            

print("Adult: "+str(i))
print("Child: "+str(j))