from project import ResultValues

from id3.test_public_bin import donnees as test_data

arbre = ResultValues().arbre

"""
print('Arbre de décision :')
print(arbre)
print()"""

for d in test_data:
    print("Was: " + arbre.classifie(d[1]) + "Expected: " + d[0])