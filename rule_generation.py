from id3.moteur_id3 import noeud_de_decision



class RuleGenerator():

  def rec(self, arbre, partial_rule):
    if arbre.terminal() :
      list_rules = [[partial_rule,"test_classe"]]#arbre.classe]
    else :
      list_rules = []
      dict_ = arbre.enfants
      for key, child in dict_.items():
        string = "test"#str(arbre.attribut) + " = " + key.str()
        list_rules = list_rules + self.rec(child, partial_rule + [string])
    return list_rules

  def __init__(self, arbre):
    self.rules = self.rec(arbre, [])