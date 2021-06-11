#Cosine similarity and cosine similarity with synonyms
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from collections import Counter
import string
from nltk.corpus import wordnet

def get_word_synonyms_from_sent(word):
    word_synonyms = []
    for synset in wordnet.synsets(word):
        for lemma in synset.lemma_names():
            word_synonyms.append(lemma)
    return word_synonyms

def get_tokens(text):


    lowers = text.lower()
    #remove the punctuation using the character deletion step of translate
    no_punctuation = lowers.translate( string.punctuation)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens

def cosine1(ans, ans1):
    vect = TfidfVectorizer(min_df=1)
    #ans="European officials sought to deflect mounting pressure from world leaders, warning of a long road ahead to end the region's debt crisis. " 
     #   "convert light energy into chemical energy that can later be released to fuel the organisms activities"
    #ans1="World leaders meeting at a G20 summit in Mexico have urged Europe to take all necessary measures to overcome the eurozone debt crisis"

    tokens = get_tokens(ans)
    tokens1=get_tokens(ans1)
    filtered = [w for w in tokens if not w in stopwords.words('english')]
    filtered1=[w for w in tokens1 if not w in stopwords.words('english')]

    #print(filtered)
    #print(filtered1)
    A1=' '.join(str(k) for k in filtered)
    B1=' '.join(str(k) for k in filtered1)
    C1=[]
    D1=[]
    for i in filtered:
        C1=C1+get_word_synonyms_from_sent(i)
    for i in filtered1:
        D1=D1+get_word_synonyms_from_sent(i)
    #print(C1)
    #print(D1)
    A2=' '.join(str(k) for k in C1)
    B2=' '.join(str(k) for k in D1)
    count = Counter(filtered)
    #print(count)

    tfidf = vect.fit_transform([A1,B1])
    print("Cosine Similarity:"+str((tfidf * tfidf.T).A[0,1]*100)+"%")
    return (tfidf * tfidf.T).A[0,1]*100

    tfidf = vect.fit_transform([A2,B2])
    print((tfidf * tfidf.T).A[0,1])
    return (tfidf * tfidf.T).A[0,1]