##############################################################
# ToDo: We could have a seperate tag list that can be ignored.
#
##############################################################

import os 
import json
import operator
#import spellcorrector
import re, collections      #for spell corrections
from difflib import SequenceMatcher

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
#DICTIONARY_OF_WORDS_FILE = '../resources/big.txt_v2'
#DICTIONARY_OF_WORDS_FILE = '../resources/aa.txt'
#NWORDS = train(words(file(DICTIONARY_OF_WORDS_FILE).read()))  # Depricated in Python 3.x
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
    data = json.loads(fp.read())        # this returns a list

    return (data)

####################################################
# Find possible corrections and dump to a text file
####################################################
def FindCorrections(all_words_list):
    outfile = open("corrections.txt", "w")
    # tag words that had no corrections
    # These can be correctly spelled words and
    # special group of words (with accents etc) that
    # the corpus has no suggestions for.
    outfile_other = open("no_corrections.txt", "w")
    
    outfile.write(" WORD -> SUGGESTION  [FUZZINESS SCORE] \n")
    for k in sorted(all_words_list):
        cw = correct(k)
        # NB: words should be hashable for the sequence matcher to work
        m = SequenceMatcher(None, k, cw)
        r = m.ratio()
        msg = k + " -> " + cw + "\t [fuzz: " + str(round(r,2)) + "]"

        if k is cw:
            #print("%s -> %s [fuzz: %f]" % (k, cw, r ))
            #outfile.write("%s -> %s [fuzz: %f]\n" % (k, cw, r ))
            #outfile.write(msg.decode('iso-8859-1').encode('utf-8'))
            #outfile.write(msg)
            outfile_other.write(k + "\n")
        else:
            print("[C] %s -> %s [fuzz: %f]" % (k, cw, r))
            #outfile.write("[C] %s -> %s [fuzz: %f]\n" % (k, cw, m.ratio() ))
            msg1 = "[C] " + msg + "\n"
            #outfile.write(msg1.decode('iso-8859-1').encode('utf-8'))
            outfile.write(msg1)

        
    outfile.close()
    outfile_other.close()

#################################################
# Find Possible Duplicates
#################################################
def Duplicates(words_list):
    outfile = open("duplicates.txt", "w")
    outfile_other = open("no_duplicates.txt", "w")
    outfile.write(" WORD -> SUGGESTION/S \n")
    MIN_MATCH_RATIO = 0.75          # Level of similarity to call a duplicate
                                    # 0.75 is by trail and error
    dups_dict = dict()
    for w1 in sorted(words_list):
        dups_dict[w1] = list()
        
        for w2 in words_list:
            if w2 not in dups_dict.keys():
                # Automatics junk heurisitcs is disabled as we do not expect such
                # NB: words should be hashable for sequence matching to work
                m = SequenceMatcher(None, w1, w2)
                r = m.ratio()
                if r > MIN_MATCH_RATIO:     # assume closely matching
                    dups_dict[w1].append(w2)       
                    msg = w1 + " -> " + w2 + "[fuzz: " + str(round(r,2)) + "]"
                    #print(msg)
                    #outfile.write(msg)

    count = 0
    for k in sorted(dups_dict.keys()):
        v = dups_dict[k]
        #outfile.write()
        if len(v)>0:
            count += 1
            #print(" %s : " % v, end="")
            #print (sorted(v))
            m = SequenceMatcher(None, k, w2)
            r = m.ratio()

            msg = "[D] " + k + " -> "
            msg += ", ".join(sorted(v)) + "\n"
            outfile.write(msg)
        else:
            outfile_other.write(k + "\n")

    print ("Possible duplicate words estimate: % i" % count)
    #print(dups_dict)
    outfile.close()
    outfile_other.close()
    
#####################################################
#   Print Most Frequent Tags
#####################################################
def TopTen(words_dict):
    sorted_word_list = sorted(words_dict.items(), key=operator.itemgetter(1), reverse=True)
    #print (all_words_dic)
    #print (sorted_word_list)
    counter = 0
    print (" ********* 10 most frequent tags (before corrections) ******** ")
    for w in sorted_word_list:
        print (w)
        counter +=  1
        if (counter >=10):
            break
    print (" ************************************************************* \n")


#####################################################
#                 M   A   I   N
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

    # Print Top Ten tags (before corrections)               
    TopTen(all_words_dic)
    FindCorrections(list(all_words_dic.keys()))
    Duplicates(all_words_dic.keys())
    
    #print("alpha_words: %d" % len(alpha_words_dic))
    #print(alpha_words_dic)
    #print("alphanum_words: %d" % len(alphanum_words_dic))
    print(alphanum_words_dic)
    #print("hyp_words: %d" % len(hyp_words_dic))
    #print(hyp_words_dic)
    print("Other words: %d" % len(other_words_dic))
    print(other_words_dic)

