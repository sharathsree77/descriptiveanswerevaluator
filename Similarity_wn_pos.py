from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
 
def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
 
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))
 
    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
 
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
 
    score, count = 0.0, 0
 
    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        simlist = [synset.path_similarity(ss) for ss in synsets2 if synset.path_similarity(ss) is not None]
        if not simlist:
            continue;
        best_score = max(simlist)
        #best_score = max([synset.path_similarity(ss) for ss in synsets2])
 
        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1
 
    # Average the values
    if(count==0):
       return 0
    else:
        score /= count
        return score*100
 
def similarityMatcher(sentences, focus_sentence):
    #sentences=["Photosynthesis is a process used by plants and other organisms to " \
    #    "convert light energy into chemical energy that can later be released to fuel the organisms activities"]
 
    #focus_sentence = "Photosynthesis is step used by plants to convert light energy into chemical energy"
    
    #print(sentences+ focus_sentence)
    #print("Similarity(\"%s\", \"%s\") = %s %%" % (focus_sentence, sentences, sentence_similarity(focus_sentence, sentences)))
    print("Semantic Similarity:"+str(sentence_similarity(focus_sentence, sentences))+"%")
    return(sentence_similarity(focus_sentence, sentences))
    #return("Similarity(\"%s\", \"%s\") = %s %%" % (focus_sentence, sentences, sentence_similarity(focus_sentence, sentences)))
    for sentence in sentences:
        print("Similarity(\"%s\", \"%s\") = %s" % (focus_sentence, sentence, sentence_similarity(focus_sentence, sentence)))
        #return ("Similarity(\"%s\", \"%s\") = %s" % (focus_sentence, sentence, sentence_similarity(focus_sentence, sentence)))
        #print ("Similarity(\"%s\", \"%s\") = %s" % (sentence, focus_sentence, sentence_similarity(sentence, focus_sentence)))
        print 
        
    def symmetric_sentence_similarity(sentence1, sentence2):
        """ compute the symmetric sentence similarity using Wordnet """
        return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) / 2 
 
    for sentence in sentences:
        print ("SymmetricSimilarity(\"%s\", \"%s\") = %s" % (focus_sentence, sentence, symmetric_sentence_similarity(focus_sentence, sentence)))
        #print ("SymmetricSimilarity(\"%s\", \"%s\") = %s" % (sentence, focus_sentence, symmetric_sentence_similarity(sentence, focus_sentence)))
        print 

#similarityMatcher("Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy that can later be released to fuel the organisms activities", "Photosynthesis is step used by plants to convert light energy into chemical energy")
