import numpy as np

def levenshtein1(seq1, seq2):  
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    sim=matrix[size_x-1,size_y-1]
    #print(sim)
    if(len(seq1) > len(seq2)):
        max = len(seq1)
    else:
        max = len(seq2)
    result =((max-sim)/max)*100
    print("Levenshtein Similarity:"+str(result)+"%")
    return (result)
#levenshtein1("World leaders meeting at a G20 summit in Mexico have urged Europe to take all necessary measures to overcome the eurozone debt crisis","European officials sought to deflect mounting pressure from world leaders,warning of a long road ahead to end the region's debt crisis")
