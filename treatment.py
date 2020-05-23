from id3.moteur_id3 import noeud_de_decision

class Treatment():
    
    def treatment(self, donnees, num_treats, rules):
        result=0
        for donnee in donnees:
            changes=0
            while changes <=num_treats:
                if func(donnee, rules) == 0 and changes == 0:
                    #patient is not sick
                    break
                elif func(donnee, rules) == 1:
                    changedonnee(donnee)
                    
                changes+=1

        return 0


    
    def __init__(self, donnees, rules):
        self.treat = self.treatment(donnees,0, rules)