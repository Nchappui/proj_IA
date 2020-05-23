from id3.moteur_id3.id3                     import ID3
from id3.moteur_id3_continu.id3_continuous  import ID3_continuous   as ID3_C
from id3.train_bin                          import donnees          as train_data
from id3.test_public_bin                    import donnees          as test_data
from rule_generation                        import *
from treatment                              import *


class ResultValues():

    def __init__(self):
        
        def getPrecision():
            total=0
            correct=0
        
            for d in test_data:
                total += 1
                if self.arbre.classifie(d[1])[-1] == d[0]:
                    correct += 1
            return (correct/total)
        
        id3 = ID3()

        # Task 1
        self.arbre = id3.construit_arbre(train_data)
        self.max_height=self.arbre.get_max_height()
        self.mean_height=self.arbre.get_mean_height()
        self.child_num=self.arbre.child_num()
        # Task 2
        self.precision=getPrecision()
        # Task 3
        self.faits_initiaux = None
        self.regles = RuleGenerator(self.arbre).rules
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]


rules = ResultValues().regles

"""
text_rules = '\n'.join(map(str, rules))
print(text_rules)

print("-----------------------------------")

explain = getRuleFromExample(rules,train_data[7][1])
print(explain)#'\n'.join(map(str, explain)))
print(explain in rules)

all_ = all(getRuleFromExample(rules, dataPoint[1]) in rules for dataPoint in train_data)
print(f"is getRuleFromExample in rules for all rules ?: {all_}")

print("-----------------------------------")

print(explainRuleFromExample(rules,test_data[0][1]))

print("-----------------------------------")

test_stripped = map(lambda pair: pair[1], test_data)
treated = Treatment(train_data, rules).treatment(test_stripped)
count=0
for treat in treated:
    count+=1
    print(treat)
print("Cas soignés:")
print(count)
"""
