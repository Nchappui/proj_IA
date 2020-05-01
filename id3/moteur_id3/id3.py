from math import log
from .noeud_de_decision import NoeudDeDecision

class ID3:
    """ Algorithme ID3. """
    
    def construit_arbre(self, donnees):
        """ Construit un arbre de décision à partir des données d'apprentissage.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        
        # Nous devons extraire les domaines de valeur des 
        # attributs, puisqu'ils sont nécessaires pour 
        # construire l'arbre.
        attributs = {}
        for donnee in donnees:
            for attribut, valeur in donnee[1].items():
                valeurs = attributs.get(attribut)
                if valeurs is None:
                    valeurs = set()
                    attributs[attribut] = valeurs
                valeurs.add(valeur)
            
        arbre = self.construit_arbre_recur(donnees, attributs)
        
        return arbre

    def construit_arbre_recur(self, donnees, attributs):
        """ Construit rédurcivement un arbre de décision à partir 
            des données d'apprentissage et d'un dictionnaire liant
            les attributs à la liste de leurs valeurs possibles.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :param attributs: un dictionnaire qui associe chaque\
            attribut A à son domaine de valeurs a_j.
            :param list classes:
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        
        allInSameC = all(map(lambda d: d[0] == donnees[0][0], donnees))

        if(allInSameC):
            return NoeudDeDecision(None,donnees) #Leaf
        else:
            attrToH = {attribut: h_C_A(donnees, attribut, valeurs) for attribut, valeurs in attributs.items()}

            bestAttr = max(attrToH, key = lambda key: attrToH[key])

            valeurs = attributs[bestAttr]

            partition = partitionne(donnees, bestAttr, valeurs)

            childDict = { v: construit_arbre_recur(partition[v], attributs) for v in valeurs }
            return NoeudDeDecision(bestAttr,donnees,)



    def partitionne(self, donnees, attribut, valeurs):
        """ Partitionne les données sur les valeurs a_j de l'attribut A.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: un dictionnaire qui associe à chaque valeur a_j de\
            l'attribut A une liste l_j contenant les données pour lesquelles A\
            vaut a_j.
        """
        def split(valeur):
            valeur: filter(lambda x: x[1][attribut] == valeur, donnees)
        return map(split,valeurs)

    def p_aj(self, donnees, attribut, valeur):
        """ p(a_j) - la probabilité que la valeur de l'attribut A soit a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.            
            :return: p(a_j)
        """

        return len(filter(lambda x: x[1][attribut] == valeur, donnees))/len(donnees)

    def p_ci_aj(self, donnees, attribut, valeur, classe):
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | a_j)
        """

        knowingAj = filter(lambda x: x[1][attribut] == valeur, donnees)
        return len(filter(lambda x: x[0] == classe, knowingAj))/len(knowingAj)

    def h_C_aj(self, donnees, attribut, valeur):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: H(C|a_j)
        """

        classes = map(lambda d: d[0], donnees).unique

        def test(classe):
            p = p_ci_aj(donnees,attribut,valeur, classe)
            p * log(p)
        
        proto = map(test, classes)

        return -sum(proto)

    def h_C_A(self, donnees, attribut, valeurs):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.
            
            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :param list classes: liste des classes possible
            :return: H(C|A)
        """

        return sum(map(lambda valeur: h_C_aj(donnees, attribut, valeur), valeurs))