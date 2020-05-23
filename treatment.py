from id3.moteur_id3 import noeud_de_decision

class Treatment():
    
    def treatment(self, donnees, num_treats, rules):
        result=0
        for donnee in donnees:
            changes=0
            while changes <=num_treats:
                if self.func(donnee, rules) == 1:
                    self.changedonnee(donnee, changes)

                else:
                    #patient is not sick anymore
                    result +=1

        return 0


    
    def __init__(self, donnees, rules):
        self.treat = self.treatment(donnees,0, rules)

    def func(self, donnee, rules):
        #just to remove errors
        return 1

    def changedonnee(self, donnee, changes):
        #changes a donne and updates the number of changes made
        return 1