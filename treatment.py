from id3.moteur_id3 import noeud_de_decision

class Treatment():
    
    def treatment(self, donnees, num_treats, rules):
        result=0
        for donnee in donnees:
            changes=1
            while changes <=num_treats and donnee[0]==1:
                if changes == 1:
                    #change one attribute
                    for key, value in donnee[1].items():
                        if key !='age' or key !='sex':
                            
                            if explaineWithRule(donnee[0],rules)[-1] == 0:
                                #patient soigne
                                result +=1
                                changes=3
                                break
                    
                    
                elif changes ==2:
                    #change two attributes
                    for key, value in donnee[1].items():
                        if key !='age' or key !='sex':
                            value +=1

                changes +=1
        return result


    
    def __init__(self, donnees, rules):
        self.treat = self.treatment(donnees,0, rules)

    def func(self, donnee, rules):
        #just to remove errors
        return 1
