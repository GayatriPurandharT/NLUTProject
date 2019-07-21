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

    if definition is None:
        return [ '--- No definition found for pos_key %s ---' % pos_key ] 
    return definition

from processed_stuff import data

final_data = []
with open('final_dictionary.csv', mode='w') as f:
    count = 0
    for base_word, pos_tags in data.items():
        # for base_word, pos_tags in d:
        print('-', base_word)
        for pos_tag, info in pos_tags.items():
            word =  info['word']
            pos_key = info['pos_key']
            definition = get_definition(base_word, pos_key)

            line = "%s,\t%s,\t%s,\t%s" % (base_word, pos_tag, word, ';'.join(definition))

            print(line)
            f.write(line)
            f.write("\n")
            f.flush()
            count = count + 1
            print("----------------- %d ----------------" % count)
print("-----Done!------")
