from id3.moteur_id3.id3  import ID3
from id3.train_bin       import donnees as train_data
from id3.test_public_bin       import donnees as test_data
from rule_generation     import *
from treatment           import *


class ResultValues():

    def __init__(self):
        
        # Do computations here
        
        id3 = ID3()

        # Task 1
        self.arbre = id3.construit_arbre(train_data)
        # Task 3
        self.faits_initiaux = None
        self.regles = RuleGenerator(self.arbre).rules
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]


rules = ResultValues().regles

text_rules = '\n'.join(map(str, rules))
print(text_rules)
"""
print("-----------------------------------")

explain = getRuleForExample(rules,train_data[7][1])
print(explain)#'\n'.join(map(str, explain)))
print(explain in rules)

all_ = all(getRuleFromExample(rules, dataPoint[1]) in rules for dataPoint in train_data)
print(f"is getRuleFromExample in rules for all rules ?: {all_}")

print("-----------------------------------")

print(explainRuleFromExample(rules,train_data[7][1]))
"""
print("-----------------------------------")

test_stripped = map(lambda pair: pair[1], train_data)
treated = Treatment(train_data, rules).treatment(test_stripped)
count=0
for treat in treated:
    count+=1
    print(treat)
print("Cas soignés:")
print(count)