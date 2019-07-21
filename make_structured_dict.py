import csv
import sys
from PyDictionary import PyDictionary

dictionary=PyDictionary()
def get_definition(word, pos_key, dictionary=dictionary):
    # TODO: Handle case where pos isn't mapped to a definition key.

    # Mapping the part of speech of the base word to the definition keys
    # that are used in the dictionary.
    key_mapping = {
            # 'm': 'Noun', # TODO: noun or adjective.
            # 'i': 'preposition',
            'n': 'Noun',
            'v': 'Verb',
            'j': 'Adjective',
            # 'x': 'exclamation',
            # 'd': 'personal pronoun',
            'a': 'Adverb',
            }
    meaning = dictionary.meaning(word)

    pos = key_mapping.get(pos_key, None)

    definition = None
    if (meaning is not None) and (pos is not None):
        try:
            definition = meaning[pos]
        except Exception as e:
            print(e)

    # if pos is None:
    #     return None

    if definition is None:
        print('No definition found.')
        print(pos_key, pos, meaning)
        return '--- No definition found for pos_key %s ---' % pos_key 
    return definition

def process_csv_row(row):
    # TODO: handle <g\>
    # Check if the row has all the required data.
    if len(row) < 3:
        print('No meaningful data in row', row)
        return None

    word = row[0]
    base_word = row[2].strip()[:-2]
    pos_key = row[2].strip()[-1] # we'll use this value to get definition key based on pos.
    pos_tag = row[1]     # actual pos tag we'll be storing.
    return word, base_word, pos_key, pos_tag

def process_row(row):
    # Getting meaningful data from row.
    _data = process_csv_row(row)
    if _data is None:
        print("Can not process row.", row)
        return None

    word, base_word, pos_key, pos_tag = _data

    # definition = get_definition(base_word, pos_key)

    return {
            'word': word,
            'base_word': base_word,
            'pos_tag': pos_tag,
            'pos_key': pos_key,
            # 'def': definition
            }

if __name__ == '__main__':
    processed_rows = []
    base_words = {}
    with open('./lexicon.txt', mode='r') as f:
        csv_reader = csv.reader(f, delimiter='\t')
        count = 0
        for row in csv_reader:
            print(count, "------------------------------------------------------")
            print(row)

            processed_row = process_row(row)
            if processed_row is None: continue
            print(processed_row)

            processed_rows.append(processed_row) # not using.

            if processed_row['base_word'] not in  base_words:
                base_words[processed_row['base_word']] = {}

            # if processed_row['pos_tag'] not in base_words[processed_row['base_word']]:
            #     base_words[processed_row['base_word']][processed_row['pos_tag']] = []

            # base_words[processed_row['base_word']][processed_row['pos_tag']].append(processed_row)
            base_words[processed_row['base_word']][processed_row['pos_tag']] = processed_row

            count += 1
            print("------------------------------------------------------")

    with open('./processed_stuff.py', mode='w') as f:
        # f.write("data =" + str(processed_rows))
        f.write("data =" + str(base_words))

    print('----- Done! -----')
    
