def sim(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))
def jaccard1(a,b):
    #a="hi, am there"
    #b="hello, am are you"
    list1=a.split()
    list2=b.split()

    words1 = set(list1)
    words2 = set(list2)
    print("Jaccard Similarity:"+str(sim(words1, words2)*100)+"%")
    return(sim(words1,words2)*100)