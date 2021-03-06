from math import log
from .noeud_de_decision_continu import NoeudDeDecision

class ID3_continuous:
   
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
        seuilsDict = {}
        for donnee in donnees:
            for attribut, seuil in donnee[1].items():
                valeurs = seuilsDict.get(attribut)
                if valeurs is None:
                    valeurs = set()
                    seuilsDict[attribut] = valeurs
                valeurs.add(seuil)

        # Find the predominant class
        classes = set([row[0] for row in donnees])
        # print(classes)
        predominant_class_counter = -1
        for c in classes:
            # print([row[0] for row in donnees].count(c))
            if [row[0] for row in donnees].count(c) >= predominant_class_counter:
                predominant_class_counter = [row[0] for row in donnees].count(c)
                predominant_class = c
        # print(predominant_class)
            
        arbre = self.construit_arbre_recur(donnees, seuilsDict, predominant_class)

        return arbre

    def construit_arbre_recur(self, donnees, seuilsDict, predominant_class):
        """ Construit récursivement un arbre de décision à partir 
            des données d'apprentissage et d'un dictionnaire liant
            les attributs à la liste de leurs valeurs possibles.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :param attributs: un dictionnaire qui associe chaque\
            attribut A à son domaine de valeurs a_j.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        
        def classe_unique(donnees):
            """ Vérifie que toutes les données appartiennent à la même classe. """
            
            if len(donnees) == 0:
                return True 
            premiere_classe = donnees[0][0]
            for donnee in donnees:
                if donnee[0] != premiere_classe:
                    return False 
            return True

        if donnees == []:
            return NoeudDeDecision(None, None, [str(predominant_class), dict()], str(predominant_class))

        # Si toutes les données restantes font partie de la même classe,
        # on peut retourner un noeud terminal.
        elif classe_unique(donnees):
            return NoeudDeDecision(None, None, donnees, str(predominant_class))
            
        else:
            # Sélectionne l'attribut qui réduit au maximum l'entropie.
            h_C_As_attribs = [(self.min_h_C_A(donnees, attribut, seuils), 
                               attribut) for attribut, seuils in seuilsDict.items()]

            minSol = min(h_C_As_attribs, key=lambda h_a: h_a[0][0])
            attribut = minSol[1]
            seuil = minSol[0][1]

            partitions = self.partitionne(donnees, attribut, seuil)
            
            def partToChild(part):
                return self.construit_arbre_recur(part, seuilsDict, predominant_class)

            enfants = list(map(partToChild, partitions))

            return NoeudDeDecision(attribut, seuil, donnees, str(predominant_class), enfants)

    def partitionne(self, donnees, attribut, seuil):
        """ Partitionne les données sur la valeur de seuil.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param valeur_seuil
            :return: une pair de listes, la première dont tous les éléments sont plus petits que le seuil et la deuxième avec des elements plus grands
        """

        partition = ([], [])
        for donnee in donnees:
            valeur = donnee[1][attribut]
            partition[valeur <= seuil].append(donnee)
        
        return partition

    def p_aj(self, donnees, attribut, seuil):
        """ p(a_j) - les probabilité que la valeur de l'attribut A soit en dessous du seuil et en dessus du seuil

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param seuil: la valeur de seuil           
            :return: p(a_j soit en dessous, a_j soit en dessus)
        """
        # Nombre de données.
        nombre_donnees = len(donnees)
        
        # Permet d'éviter les divisions par 0.
        if nombre_donnees == 0:
            return (0.0, 0.0)
        
        #Probabilite de tomber en dessus et en dessous du seuil
        probabilities = map(lambda part: len(part)/nombre_donnees, self.partitionne(donnees, attribut, seuil))
        return probabilities

    def p_ci_aj(self, donnees, attribut, seuil, classe):
        """ p(c_i|a_j) - les probabilités conditionnelles que la classe C soit c_i\
            étant donné que l'attribut A soit respectivement en dessus et en dessous du seuil.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param seuil: la valeur du seuil.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | < seuil),p (c_i | > seuil)
        """
        parts = self.partitionne(donnees, attribut, seuil)
        nombre_ajs = map(lambda part: len(part), parts)
        
        # Nombre d'occurrences de la classe c_i parmi les données pour lesquelles 
        # A vaut a_j.
        donnees_cis = map(lambda part: filter(lambda donnee: donnee[0] == classe, part), parts)
        nombre_cis = map(lambda part: len(list(part)), donnees_cis)

        # p(c_i|a_j) = nombre d'occurrences de la classe c_i parmi les données 
        #              pour lesquelles A vaut a_j /
        #              nombre d'occurrences de la valeur a_j parmi les données.
        def map_(pair):
            nombre_ci = pair[0]
            nombre_aj = pair[1]
            if(nombre_aj == 0):
                return 0.0
            else:
                return nombre_ci / nombre_aj
        
        return map(map_, zip(nombre_cis, nombre_ajs))

    def h_C_aj(self, donnees, attribut, seuil):
        """ H(C|a_j) - les entropies de la classe parmi les données pour lesquelles\
            l'attribut A est respectivement en dessous et en dessus du seuil.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param seuil: la valeur du seuil.
            :return: H(C | < seuil), H(C | > seuilS)
        """
        # Les classes attestées dans les exemples.
        classes = list({donnee[0] for donnee in donnees})
        
        # Calcule p(c_i|a_j) pour chaque classe c_i.
        p_ci_ajs_beneath = [list(self.p_ci_aj(donnees, attribut, seuil, classe))[0]
                    for classe in classes]
        p_ci_ajs_above = [list(self.p_ci_aj(donnees, attribut, seuil, classe))[1]
                    for classe in classes]
        
        # Si p vaut 0 -> plog(p) vaut 0.
        def computeH(p_ci_ajs):
            def compute(p_ci_aj):
                return p_ci_aj * log(p_ci_aj, 2.0)
            list_ = [compute(p_ci_aj) for p_ci_aj in p_ci_ajs if p_ci_aj != 0]
            return -sum(list_)
        h_C_ajs = map(computeH, [p_ci_ajs_beneath, p_ci_ajs_above])

        return h_C_ajs

    def h_C_A(self, donnees, attribut, seuil):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.
            
            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param seuil: la valeur du seuil.
            :return: H(C| < seuil), H(C| > seuil)
        """
        # Calcule P(a_j) pour chaque valeur a_j de l'attribut A.
        #p_ajs = [self.p_aj(donnees, attribut, seuil) for valeur in valeurs]
        p_ajs = list(self.p_aj(donnees, attribut, seuil))

        # Calcule H_C_aj pour chaque valeur a_j de l'attribut A.
        #h_c_ajs = [self.h_C_aj(donnees, attribut, seuil) 
        #           for valeur in valeurs]
        h_c_ajs = list(self.h_C_aj(donnees, attribut, seuil))

        return sum([p_aj * h_c_aj for p_aj, h_c_aj in zip(p_ajs, h_c_ajs)])

    def min_h_C_A(self, donnees, attribut, seuils):
        h_C_As = map(lambda seuil: (self.h_C_A(donnees, attribut, seuil), seuil), seuils)

        min_h_C_A = min(h_C_As, key = lambda pair: pair[0])
        return min_h_C_A

