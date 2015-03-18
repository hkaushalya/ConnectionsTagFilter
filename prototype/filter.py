import os 
import json
import operator
#import spellcorrector
import re, collections

#from nltk.corpus import gutenberg

#### NEED SEPARATE MODULE ####

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

print ("Current Directory: %s " % os.getcwd())
DICTIONARY_OF_WORDS_FILE = '../resources/big.txt'
#NWORDS = train(words(file(DICTIONARY_OF_WORDS_FILE).read()))
NWORDS = train(words(open(DICTIONARY_OF_WORDS_FILE).read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)


#############################




#####################################################
# Search for given set of characters in a string
# Return True if anyone of the charactors is found.
# Else returns False
#####################################################
def HasChars(s, st):
    #s: string
    # st: a set
    for c in st:
        if c in s:
            return True

    return False

#####################################################
# Retrieve JSON data from file
#####################################################
def GetData():
    fp = ""
    #filename = "../resources/profileTags.json"
    #filename = "../resources/tags.json"
    filename = "../resources/profileTags_fixed.json"

    try:
        fp = open(filename)
        print ("Opened file %s" % filename)
    except IOError:
        print ("File not found!")

    lines = 0
    for line in fp.readlines():
        lines += 1
        #print (line)
        
    print("%i lines of data in file %s" % (lines,  filename))
    fp.seek(0)                          # reset read head to start
    data = json.loads(fp.read())        #this returns a list

    return (data)


#####################################################
#       M   A   I   N
#####################################################

if __name__ == "__main__":

    #Current working directory
    print ("Current Directory: %s " % os.getcwd())

    data = GetData()
    #print (data)

    #################################################
    # Categorize and store tags in dictionaries
    #################################################
    all_words_dic = dict()
    alpha_words_dic = dict()    # words with alpha
    alphanum_words_dic = dict() # anything with numbers. no suggestions/only duplicate search
    hyp_words_dic = dict()      # words with hyphans
    other_words_dic = dict()      # anything else left

    for d in data:
        #print (d)
        #print (type(d))
        for k,v in d.items():
            #print (k)
            if (k == 'Tags'):
                for wd in v:
                    t = wd.lower()
                    #print (t)
                    if t in all_words_dic:
                        all_words_dic[t] += 1
                    else:
                        all_words_dic[t] = 1

                    # categorizing and storing in difffernt dictionaries
                    if t.isalpha():
                        if t in alpha_words_dic:
                            alpha_words_dic[t] += 1
                        else:
                            alpha_words_dic[t] = 1

                    elif t.isalnum():
                        if t in alphanum_words_dic:
                            alphanum_words_dic[t] += 1
                        else:
                            alphanum_words_dic[t] = 1

                    elif HasChars(str(t), set('-_.')):
                        if t in hyp_words_dic:
                            hyp_words_dic[t] += 1
                        else:
                            hyp_words_dic[t] = 1

                    else:
                        if t in other_words_dic:
                            other_words_dic[t] += 1
                        else:
                            other_words_dic[t] = 1
                                  
    ###########  Now we have all the tags  ##############
                            
    sorted_word_list = sorted(all_words_dic.items(), key=operator.itemgetter(1), reverse=True)
    #print (all_words_dic)
    #print (sorted_word_list)
    counter = 0
    print (" ********* 10 most frequent tags ******** ")
    for w in sorted_word_list:
        print (w)
        counter +=  1
        if (counter >=10):
            break
    print (" **************************************** ")
        
    print("alpha_words: %d" % len(alpha_words_dic))
    #print(alpha_words_dic)
    print("alphanum_words: %d" % len(alphanum_words_dic))
    print(alphanum_words_dic)
    print("hyp_words: %d" % len(hyp_words_dic))
    #print(hyp_words_dic)
    print("Other words: %d" % len(other_words_dic))
    print(other_words_dic)


    for k,v in all_words_dic.items():
        cw = correct(k)
        if k is cw:
            continue
        else:
            print("%s -> %s" % (k, correct(k)))
        

