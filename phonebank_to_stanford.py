import pprint
pp = pprint.PrettyPrinter()

def build_datum():
    return  { 'dialogue': None, 'mor': None, 'gra': None }

def phonebank_gra_to_stanford_gra(words, gra):
    mapping_phonebank_to_stanford = {
            'SUBJ': 'nsubj', # 'nsubjpass'
            'CSUBJ': 'csubj', # 'csubjpass'
            'COBJ': 'cobj',
            'OBJ2': 'iobj',
            'JCT': 'advmod',
            'COMP': 'xcomp',
            'CONJ': 'conj',
            'OBJ': 'dobj',
            'MOD': 'nmod', # xmod amod
            'POBJ': 'call', # ?
            'INF': 'mark', 
            'LP': 'punck', # ?
            'INCROOT': 'root',
            'ROOT': 'root',
            'DET': 'det',
            'QUANT': 'nummod',
            'NEG': 'neg',
            'ENUM': 'nummod',
            'NAME': 'name', 

            # TODO
            'PUNCT': 'punct',
            'AUX': 'aux'
            }
    stanford_gra = ''
    for gra_item in gra.split(' '):
        arg0, arg1, func = gra_item.split('|')

        arg0_word = words[int(arg0) - 1]
        if(arg1 == '0'):
            arg1_word  = 'ROOT'
        else:
            arg1_word = words[int(arg1) - 1]

        stanford_func = mapping_phonebank_to_stanford.get(func)
        stanford_gra += "%s(%s, %s) " % (stanford_func, arg1_word, arg0_word) 

        if stanford_func is None:
            print("Couldn't find gra for", gra_item)
            return None

    return stanford_gra

def split_dialogue(dialogue):
    words = dialogue.split(' ')
    final_words = []
    for key, value in enumerate(words):
        if value.lower() == 'wanna':
            final_words.append('want')
            final_words.append('to')
        elif value.lower() == 'gonna':
            final_words.append('going')
            final_words.append('to')

        elif value.lower() == "i'm":
            final_words.append('I')
            final_words.append('am')

        elif value.lower() == "you're":
            final_words.append('you')
            final_words.append('are')
        elif value.lower() == "we're":
            final_words.append('we')
            final_words.append('are')
        elif value.lower() == "they're":
            final_words.append('they')
            final_words.append('are')

        elif value.lower() == "ain't":
            final_words.append('am')
            final_words.append('not')
        elif value.lower() == "can't":
            final_words.append('can')
            final_words.append('not')
        elif value.lower() == "don't":
            final_words.append('do')
            final_words.append('not')
        elif value.lower() == "didn't":
            final_words.append('did')
            final_words.append('not')
        elif value.lower() == "doesn't":
            final_words.append('does')
            final_words.append('not')
        elif value.lower() == "haven't":
            final_words.append('have')
            final_words.append('not')
        elif value.lower()[-3:] == "n't":
            final_words.append(value[:-3])
            final_words.append("not")

        elif value.lower()[-3:] == "'ll":
            final_words.append(value[:-3])
            final_words.append("will")

        elif value.lower() == "needta":
            final_words.append('need')
            final_words.append('to')
        elif value.lower() == "sposta":
            final_words.append('suppose')
            final_words.append('to')
        elif value.lower() == "hafta":
            final_words.append('have')
            final_words.append('to')
        elif value.lower() == "hasta":
            final_words.append('has')
            final_words.append('to')
        elif value.lower() == "hadta":
            final_words.append('had')
            final_words.append('to')
        elif value.lower() == "gotta":
            final_words.append('got')
            final_words.append('to')
        elif value.lower() == "oughta":
            final_words.append('ought')
            final_words.append('to')

        elif value.lower() == "you'd":
            final_words.append('you')
            final_words.append('would')
        elif value.lower() == "where'd":
            final_words.append('where')
            final_words.append('did')
        elif value.lower() == "we'd":
            final_words.append('we')
            final_words.append('had')
        elif value.lower() == "why'd":
            final_words.append('why')
            final_words.append('had')
        elif value.lower() == "what'd": # TODO: handling all cases?? Don't think so.
            final_words.append('what')
            final_words.append('did')

        elif value.lower() == "i've":
            final_words.append('I')
            final_words.append('have')
        elif value.lower() == "you've":
            final_words.append('you')
            final_words.append('have')
        elif value.lower() == "we've":
            final_words.append('we')
            final_words.append('have')

        elif value.lower() == "let's":
            final_words.append('let')
            final_words.append('us')
        elif value.lower() == "it's":
            final_words.append('it')
            final_words.append('is')
        elif value.lower() == "pig's":
            final_words.append('pig')
            final_words.append('is')
        elif value.lower()[-2:] == "'s":
            final_words.append(value[:-2])
            final_words.append("'s")

        else:
            final_words.append(value)

    # TODO: handle '+' signs in between combined words

    print(final_words)
    return final_words


processed_data = []
unknown_lines = []
couldnt_find_gra = []
with open('./vk.txt', mode='r') as f:
    datum = build_datum()

    for _line in f:
        line = _line.strip()
        identifier = line[0:5].strip()
        data = line[5:].strip()
        print(line)

        if(identifier == '*ADU:' or identifier == '*CHI:'):
            datum['dialogue'] = {}
            datum['dialogue']['original'] = data.strip()
            datum['dialogue']['split'] = split_dialogue(data)
        elif(identifier == '%mor:'):
            datum['mor'] = data
        elif(identifier == '%gra:'):
            datum['gra'] = {}
            stanford_gra = phonebank_gra_to_stanford_gra(datum['dialogue']['split'], data)
            if stanford_gra is None:
                pp.pprint(datum)
                couldnt_find_gra.append(data)
                datum = build_datum()
                print("Stanford gra not found!-----------------------------------")
                continue
            datum['gra']['stanford'] = stanford_gra
            datum['gra']['phonebank'] = data
        else:
            pp.pprint(datum)
            unknown_lines.append(line)
            datum = build_datum()
            print('unidentified line:', line, "-----------------------------------")
            continue
        
        if (datum['dialogue'] is not None and
                datum['mor'] is not None and
                datum['gra'] is not None):
            processed_data.append(datum)
            pp.pprint(datum)
            datum = build_datum()
            print("-----------------------------------")

with open('dependancy_relations.json', mode='w') as f:
    f.write(str(processed_data))

print('Done!')
print(len(processed_data), processed_data[0])
print(len(unknown_lines), unknown_lines[0])
print(len(couldnt_find_gra), couldnt_find_gra[0])

