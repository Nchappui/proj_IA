from id3.moteur_id3     import noeud_de_decision
from rule_generation    import *

realAttribut={'age': {'5', '1', '4', '3', '2'}, 'sex': {'1', '0'}, 'cp': {'1', '0', '3', '2'}, 'trestbps': {'5', '1', '4', '3', '2'}, 'chol': {'5', '1', '3', '2'}, 'fbs': {'1', '0'}, 'restecg': {'1', '0', '2'}, 'thalach': {'1', '4', '3', 
'2'}, 'exang': {'1', '0'}, 'oldpeak': {'5', '1', '4', '3', '2'}, 'slope': {'1', '0', '2'}, 'ca': {'1', '4', '3', '0', '2'}, 'thal': {'1', '3', '2', '0'}}

class Treatment():
    def __init__(self, donnees, rules):
        self.attributDict = self.constructAttributDict(donnees)
        self.rules = rules

    def constructAttributDict(self, donnees):
        attributs = realAttribut
        """
        for donnee in donnees:
            for attribut, valeur in donnee[1].items():
                valeurs = attributs.get(attribut)
                if valeurs is None:
                    valeurs = set()
                    attributs[attribut] = valeurs
                valeurs.add(valeur)
        print(attributs)
        """
        return attributs

    

    def modifyExample(self, example, depthLimit, acc): #[depthLimit, newAccDict] if result found, None otherwise 
        def modifyAttribut(attribut, value):                    #[depthLimit, newAccDict] if result found, None otherwise 
            values = self.attributDict[attribut]
            newValues = filter(lambda v: v != value, values)

            partialRes = []
            for nV in newValues:
                
                example[attribut] = nV
                label = getRuleFromExample(self.rules, example)[1]

                newAcc = acc + [[attribut,nV]]

                if(label == '0'):
                    example[attribut] = value
                    return [depthLimit, newAcc]
                elif(depthLimit > 0):
                    res = self.modifyExample(example, depthLimit-1, newAcc)
                    if res is not None:
                        partialRes.append(res)
            
            example[attribut] = value
            if(not partialRes):
                return None
            else:
                maxByDepth = max(partialRes, key = lambda pair: pair[0])
                return maxByDepth
        
        reses = []
        for attribut, value in example.items():
            if(attribut != 'age' and attribut != 'sex' and (attribut not in map(lambda pair: pair[0],acc))):
                
                res = modifyAttribut(attribut, value)
                if(res is not None):
                    reses.append(res)
        if(not reses):
            return None
        else:
            maxByDepth = max(reses, key = lambda pair: pair[0])
            return maxByDepth
    
    def treatment(self, examples):

        sickExamples = filter(lambda example: getRuleFromExample(self.rules, example)[1] == '1', examples)
        
        depthLimit = 1
        count=0
        treated = []

        for example in sickExamples:
            count+=1
            res = self.modifyExample(example, depthLimit, [])
            if(res is not None):
                numChanges = depthLimit - res[0] + 1
                changes = res[1]
                treated.append((example, numChanges, changes))
        return treated