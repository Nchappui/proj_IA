from id3.moteur_id3 import noeud_de_decision



class RuleGenerator():

  def rec(self, arbre, partial_rule):
    if arbre.terminal() :
      list_rules = [partial_rule,'{}'.format(arbre.classe().upper())]
    else :
      list_rules = []
      for key, child in arbre.enfants.items():
        string = '{}'.format(arbre.attribut) + " = " + key
        list_rules = list_rules + self.rec(child, partial_rule + [string])
    return list_rules

  def __init__(self, arbre):
    self.rules = self.rec(arbre, [])
