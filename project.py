from id3.moteur_id3.id3                     import ID3
from id3.moteur_id3_continu.id3_continuous  import ID3_continuous   as ID3_C
from id3.train_bin                          import donnees          as train_data
from id3.train_continuous                   import donnees          as train_data_continuous
from id3.test_public_bin                    import donnees          as test_data
from id3.test_public_continuous             import donnees          as test_data_continuous
from rule_generation                        import *
from treatment                              import *


class ResultValues():

    def __init__(self):
        
        def getPrecision(test_data, arbre):
            total=0
            correct=0
            for d in test_data:
                total += 1
                if arbre.classifie(d[1])[-1] == d[0]:
                    correct += 1
            return (correct/total)

        def getTreatment():
            test_stripped = map(lambda pair: pair[1], test_data)
            treated = Treatment(train_data, self.regles).treatment(test_stripped)
            return treated
        
        id3 = ID3()

        # Task 1
        self.arbre = id3.construit_arbre(train_data)
        self.max_height=self.arbre.get_max_height()
        self.mean_height=self.arbre.get_mean_height()
        self.child_num=self.arbre.child_num()

        # Task 2
        self.precision=getPrecision(test_data, self.arbre)

        # Task 3
        self.faits_initiaux = RuleGenerator(self.arbre).faits_initiaux
        self.regles = RuleGenerator(self.arbre).rules
        """The function getRuleFromExample in RuleGenerator takes a rule and an example as parameters and returns the rule for this example, 
            and then explainRuleFromExample takes as parameters a rule and an example and prints a nice prediction and explanation for it"""

        # Task 4
        self.traitements = getTreatment()

        # Task 5
        self.arbre_advance = ID3_C().construit_arbre(train_data_continuous)
        self.precision_advance = getPrecision(test_data_continuous, self.arbre_advance)

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
