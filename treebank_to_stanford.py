import pprint
pp = pprint.PrettyPrinter()

def build_datum():
    return  { 'dialogue': None, 'mor': None, 'gra': None }

def treebank_gra_to_stanford_gra(words, gra):
    mapping_treebank_to_stanford = {
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
            'PUNCT': 'punct'
            }
    stanford_gra = ''
    for gra_item in gra.split(' '):
        arg0, arg1, func = gra_item.split('|')

        arg0_word = words[int(arg0) - 1]
        if(arg1 == '0'):
            arg1_word  = '--root--'
        else:
            arg1_word = words[int(arg1) - 1]

        stanford_func = mapping_treebank_to_stanford.get(func)
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

        elif value.lower() == "needta":
            final_words.append('need')
            final_words.append('to')
        elif value.lower() == "sposta":
            final_words.append('suppose')
            final_words.append('to')
        elif value.lower() == "hafta":
            final_words.append('have')
            final_words.append('to')

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
with open('./vk.txt', mode='r') as f:
    datum = build_datum()

    for _line in f:
        line = _line.strip()
        identifier = line[0:5].strip()
        data = line[5:].strip()
        print(line)

        if(identifier == '*ADU:' or identifier == '*CHI:'):
            datum['dialogue'] = split_dialogue(data)
        elif(identifier == '%mor:'):
            datum['mor'] = data
        elif(identifier == '%gra:'):
            datum['gra'] = {}
            stanford_gra = treebank_gra_to_stanford_gra(datum['dialogue'], data)
            if stanford_gra is None:
                pp.pprint(datum)
                datum = build_datum()
                print("Stanford gra not found!-----------------------------------")
                continue
            datum['gra']['stanford'] = stanford_gra
            datum['gra']['treebank'] = data
        else:
            pp.pprint(datum)
            datum = build_datum()
            print('unidentified line:', line, "-----------------------------------")
            continue
        
        if (datum['dialogue'] is not None and
                datum['mor'] is not None and
                datum['gra'] is not None):
            processed_data.append(datum)
            # print(len(processed_data), ' '.join(datum['dialogue']))
            pp.pprint(datum)
            datum = build_datum()
            print("-----------------------------------")

# pp.pprint(processed_data)

