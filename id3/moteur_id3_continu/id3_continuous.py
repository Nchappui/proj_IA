from math import log
from .noeud_de_decision import NoeudDeDecision

class ID3_continuous:
    """ Algorithme ID3. 

        This is an updated version from the one in the book (Intelligence Artificielle par la pratique).
        Specifically, in construit_arbre_recur(), if donnees == [] (line 70), it returns a terminal node with the predominant class of the dataset -- as computed in construit_arbre() -- instead of returning None.
        Moreover, the predominant class is also passed as a parameter to NoeudDeDecision().
    """
    
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
            
        arbre = self.construit_arbre_recur(donnees, attributs, predominant_class)

        return arbre

    def construit_arbre_recur(self, donnees, attributs, predominant_class):
        """ Construit rédurcivement un arbre de décision à partir 
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
            return NoeudDeDecision(None, [str(predominant_class), dict()], str(predominant_class))

        # Si toutes les données restantes font partie de la même classe,
        # on peut retourner un noeud terminal.
        elif classe_unique(donnees):
            return NoeudDeDecision(None, donnees, str(predominant_class))
            
        else:
            # Sélectionne l'attribut qui réduit au maximum l'entropie.
            h_C_As_attribs = [(self.h_C_A(donnees, attribut, attributs[attribut]), 
                               attribut) for attribut in attributs]

            attribut = min(h_C_As_attribs, key=lambda h_a: h_a[0])[1]

            # Crée les sous-arbres de manière récursive.
            attributs_restants = attributs.copy()
            del attributs_restants[attribut]

            partitions = self.partitionne(donnees, attribut, attributs[attribut])
            
            enfants = {}
            for valeur, partition in partitions.items():
                enfants[valeur] = self.construit_arbre_recur(partition,
                                                             attributs_restants,
                                                             predominant_class)

            return NoeudDeDecision(attribut, donnees, str(predominant_class), enfants)

    def partitionne(self, donnees, attribut, seuil):
        """ Partitionne les données sur les valeurs a_j de l'attribut A.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param valeur_seuil
            :return: une pair de listes, la première dont tous les éléments sont plus petits que le seuil
        """

        partition = ([], [])
        for donnee in donnees:
            partition[donnee[attribut] <= seuil].append(donnee)
        
        return partition

    def p_aj(self, donnees, attribut, seuil):
        """ p(a_j) - la probabilité que la valeur de l'attribut A soit en dessous du seuil.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.            
            :return: p(a_j)
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
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | a_j)
        """
        parts = self.partitionne(donnees, attribut, seuil)
        nombre_ajs = map(lambda part: len(part), parts)

        # Nombre d'occurrences de la valeur a_j parmi les données.
        donnees_aj = [donnee for donnee in donnees if donnee[1][attribut] <= seuil]
        nombre_aj = len(donnees_aj)
        
        # Permet d'éviter les divisions par 0.
        if nombre_aj == 0:
            return 0
        
        # Nombre d'occurrences de la classe c_i parmi les données pour lesquelles 
        # A vaut a_j.
        donnees_cis = map(lambda part: filter(lambda donnee: donnee[0] == classe, part), parts)
        nombre_cis = map(lambda part: len(part), donnees_cis)

        # p(c_i|a_j) = nombre d'occurrences de la classe c_i parmi les données 
        #              pour lesquelles A vaut a_j /
        #              nombre d'occurrences de la valeur a_j parmi les données.
        def map_(pair):
            nombre_ci = pair[0]
            nombre_aj = pair[1]
            if(nombre_aj == 0):
                0.0
            else:
                nombre_ci / nombre_aj
        
        return map(map_, zip(nombre_cis, nombre_ajs))

    def h_C_aj(self, donnees, attribut, seuil):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: H(C|a_j)
        """
        # Les classes attestées dans les exemples.
        classes = list({donnee[0] for donnee in donnees})
        
        # Calcule p(c_i|a_j) pour chaque classe c_i.
        p_ci_ajs_beneath = [self.p_ci_aj(donnees, attribut, seuil, classe)[0]
                    for classe in classes]
        p_ci_ajs_above = [self.p_ci_aj(donnees, attribut, seuil, classe)[1]
                    for classe in classes]
        
        # Si p vaut 0 -> plog(p) vaut 0.
        def computeH(p_ci_ajs):
            -sum([p_ci_aj * log(p_ci_aj, 2.0) for p_ci_aj in p_ci_ajs if p_ci_aj != 0])
        h_C_ajs = map(computeH, [p_ci_ajs_beneath, p_ci_ajs_above])

        return h_C_ajs

    def h_C_A(self, donnees, attribut, seuil):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.
            
            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: H(C|A)
        """
        # Calcule P(a_j) pour chaque valeur a_j de l'attribut A.
        #p_ajs = [self.p_aj(donnees, attribut, seuil) for valeur in valeurs]
        p_ajs = self.p_aj(donnees, attribut, seuil)

        # Calcule H_C_aj pour chaque valeur a_j de l'attribut A.
        #h_c_ajs = [self.h_C_aj(donnees, attribut, seuil) 
        #           for valeur in valeurs]
        h_c_ajs = self.h_C_aj(donnees, attribut, seuil)

        return sum([p_aj * h_c_aj for p_aj, h_c_aj in zip(p_ajs, h_c_ajs)])

    def max_h_C_A(self, donnees, attribut):
        seuils = list({donnee[attribut] for donnee in donnees})
        h_C_As = map(lambda seuil: (seuil,self.h_C_A(donnees, attribut, seuil)), seuils)

        max_h_C_A = max(h_C_As, key = lambda pair: pair[1])
        return max_h_C_A

