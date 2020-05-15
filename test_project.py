from project import ResultValues

from id3.test_public_bin import donnees as test_data

arbre = ResultValues().arbre

"""
print('Arbre de décision :')
print(arbre)
print()"""

correct = 0
total = 0

for d in test_data:
    total += 1
    if arbre.classifie(d[1])[-1] == d[0]:
        correct += 1
print(correct/total)
