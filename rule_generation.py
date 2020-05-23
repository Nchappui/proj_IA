from id3.moteur_id3 import noeud_de_decision



class RuleGenerator():

  def rec(self, arbre, partial_rule):
    if arbre.terminal() :
      list_rules = [[partial_rule,'{}'.format(arbre.classe().upper())]]
    else :
      list_rules = []
      dict_ = arbre.enfants
      for key, child in dict_.items():
        string = [arbre.attribut, key]
        list_rules = list_rules + self.rec(child, partial_rule + [string])
    return list_rules

  def __init__(self, arbre):
    self.rules = self.rec(arbre, [])



def getRuleFromExample(rules, example):
  def rec(rules, example, acc):
    if(rules[0][0]):
      attibut = rules[0][0][0][0]
      valAtAttribut = example[attibut]

      def filter_(rule):
        return rule[0][0][1] == valAtAttribut

      filtered = filter(filter_, rules)

      rulesWhithoutAttribut = list(map(lambda rule: [rule[0][1:],rule[1]], filtered))
      return rec(rulesWhithoutAttribut, example, acc + [[attibut, valAtAttribut]])
    else:
      if(len(rules) == 1):
        return [acc, rules[0][1]]
      else:
        print("Rules has more than one element !")
  return rec(rules, example, [])

def ruleToString(rule):
  def map_(pair):
    return f"{pair[0]} == {pair[1]}"
  equals = map(map_, rule[0])
  return f"""if {" and ".join(equals)} then {rule[1]}"""

def explainRuleFromExample(rules, example):
  rule = getRuleFromExample(rules,example)
  return f"""Verdict is {rule[1]}, 
given by rule "{ruleToString(rule)}", 
for entry {example}"""