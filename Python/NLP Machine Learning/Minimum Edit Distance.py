import numpy, nltk
nltk.download('brown')
from nltk.corpus import brown as nltkB
from nltk.probability import FreqDist

def min_edit_dist(source, target):
 n = len(source)+1; m = len(target)+1
 DM = numpy.zeros ((n,m))

 for i in range(n):
        DM[i,0] = i
 for j in range(m):
        DM[0,j] = j

 for i in range(1,n):
    for j in range(1,m):
        if source[i-1] == target[j-1]:
            DM [i,j] = min(
                DM[i-1,j] + 1,
                DM[i-1,j-1],
                DM[i,j-1] + 1
             )
        else:
                DM [i,j] = min(
                DM[i-1,j] +1,
                DM[i-1,j-1] + 2,
                DM[i,j-1] + 1
            )

 return DM[n-1][m-1]

def min_edit_dist_table(source, target):
 n = len(source)+1; m = len(target)+1
 DM = numpy.zeros ((n,m))

 for i in range(n):
        DM[i,0] = i
 for j in range(m):
        DM[0,j] = j

 for i in range(1,n):
    for j in range(1,m):
        if source[i-1] == target[j-1]:
            DM [i,j] = min(
                DM[i-1,j] + 1,
                DM[i-1,j-1],
                DM[i,j-1] + 1
             )
        else:
                DM [i,j] = min(
                DM[i-1,j] +1,
                DM[i-1,j-1] + 2,
                DM[i,j-1] + 1
            )


 DM_String = "  * " + " ".join(target) + "\n* " + str(DM[0]).translate({ord(c): None for c in ',[].'}) + '\n'
 for i in range(1,n):
    DM_String += source[i-1] + ' ' + str(DM[i]).translate({ord(c): None for c in ',[].'}) + "\n"
 return (DM[n-1,m-1], DM_String)

if __name__ == "__main__":
    print(min_edit_dist("happy", "happen")) # should be 3
    print(min_edit_dist("actual", "natural")) # should be 3
    print(min_edit_dist("intention", "execution")) # should be 8

    print(min_edit_dist_table("happy", "happen")[1])     # Assuming table string is the second element returned
    print(min_edit_dist_table("actual", "natural")[1])
