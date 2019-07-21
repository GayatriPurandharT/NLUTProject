import nltk
from nltk.parse import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser

parser = CoreNLPParser(url='http://localhost:9000')
dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')

def parse_tokenized_text(sent):
    syntax_trees = list(parser.parse(sent.split()))
    with open('syntax_trees.txt', 'a') as f:
        for tree in syntax_trees:
            f.write("%s\n" % tree)



def dependency_parser(sent):
    parses = dep_parser.parse(sent.split())
        
    dep_trees = list([[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses])
    with open('dep_20_trees.txt', 'a') as f:
        for tree in dep_trees:
            f.write(sent+'\n')
            f.write("%s\n" % tree)





def main():

    # print(list(pos_tagger.tag('wanna play with the farm ?')))

    with open("dep_20_lines.txt") as file:
      
        for line in file:
            dependency_parser(line)
            
         


if __name__ == "__main__":

    main()