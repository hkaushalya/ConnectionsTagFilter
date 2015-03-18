import os 
import json
import operator
#from nltk.corpus import gutenberg


# Search for given set of characters in a string
# Return True if anyone of the charactors is found.
# Else returns False
def HasChars(s, st):
    #s: string
    # st: a set
    for c in st:
        if c in s:
            return True

    return False


if __name__ == "__main__":

    #Current working directory
    print ("Current Directory: %s " % os.getcwd())

    fp = ""
    #filename = "../resources/profileTags.json"
    #filename = "../resources/tags.json"
    filename = "../resources/profileTags_fixed.json"

    try:
        fp = open(filename)
        print ("opening %s" % filename)
    except IOError:
        print ("File not found!")

    lines = 0
    for line in fp.readlines():
        lines += 1
        #print (line)
    print("Lines # %i" % lines)
    fp.seek(0)
    data = json.loads(fp.read())        #this returns a list
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
                for t in v:
                    #print (t)
                    if t in all_words_dic:
                        all_words_dic[t] += 1
                    else:
                        all_words_dic[t] = 1

                    # categorizing
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
                            
    #sorted_dic = sorted(all_words_dic.items(), key=operator.itemgetter(1))
    #print (all_words_dic)
    #print (sorted_dic)
    print("alpha_words %d" % len(alpha_words_dic))
    #print(alpha_words_dic)
    print("alphanum_words %d" % len(alphanum_words_dic))
    print(alphanum_words_dic)
    print("hyp_words %d" % len(hyp_words_dic))
    #print(hyp_words_dic)
    print("Other words %d" % len(other_words_dic))
    print(other_words_dic)

