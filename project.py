from id3.moteur_id3.id3  import ID3
from id3.train_bin       import donnees as train_data
from rule_generation     import *


class ResultValues():

    def __init__(self):
        
        # Do computations here
        
        id3 = ID3()

        # Task 1
        self.arbre = id3.construit_arbre(train_data)
        # Task 3
        self.faits_initiaux = None
        self.regles = None
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]



arbre = ResultValues().arbre
rules = RuleGenerator(arbre).rules
text_rules = '\n'.join([str(i) for i in rules])
print(text_rules)