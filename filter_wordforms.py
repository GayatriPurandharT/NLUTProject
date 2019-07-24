import csv


vk_text = None
with open("./vk.txt", mode="r") as f_vk:
    vk_text =  f_vk.read().lower()

out_text = ''
with open("./final_dictionary.csv", mode="r") as f_dict:
    csv_reader = csv.reader(f_dict, delimiter=",")
    count = 0
    for row in csv_reader:
        if len(row) < 3:
            continue
        if row[2].strip().lower() in vk_text:
            out_line = ','.join(row)
            out_text += out_line + "\n"
            print(out_line)
            count += 1
with open('./final_dictionary_filtered_wordforms.csv', mode='w') as f:
    f.write(out_text)
print("-------------------------------")
print(count)
print("-------------------------------")
