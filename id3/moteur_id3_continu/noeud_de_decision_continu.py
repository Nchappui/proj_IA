class NoeudDeDecision:
    

    def __init__(self, attribut, seuil, donnees, p_class, enfants=None):
        """
            :param attribut: l'attribut de partitionnement du noeud (``None`` si\
            le noeud est un noeud terminal).
            :param list donnees: la liste des données qui tombent dans la\
            sous-classification du noeud.
            :param enfants: un dictionnaire associant un fils (sous-noeud) à\
            chaque valeur de l'attribut du noeud (``None`` si le\
            noeud est terminal).
        """

        self.attribut = attribut
        self.seuil = seuil
        self.donnees = donnees
        self.enfants = enfants
        self.p_class = p_class

    def terminal(self):
        """ Vérifie si le noeud courant est terminal. """

        return self.enfants is None

    def classe(self):
        """ Si le noeud est terminal, retourne la classe des données qui\
            tombent dans la sous-classification (dans ce cas, toutes les\
            données font partie de la même classe. 
        """

        if self.terminal():
            return self.donnees[0][0]

    def classifie(self, donnee):
        """ Classifie une donnée à l'aide de l'arbre de décision duquel le noeud\
            courant est la racine.

            :param donnee: la donnée à classifier.
            :return: la classe de la donnée selon le noeud de décision courant.
        """

        rep = ''
        if self.terminal():
            rep += 'Alors {}'.format(self.classe().upper())
        else:
            valeur = donnee[self.attribut]
            b = valeur <= self.seuil
            enfant = self.enfants[b]
            if(b):
                op = "<="
            else:
                op = ">"
            rep += f'Si {self.attribut} {op} {valeur}, '
            try:
                rep += enfant.classifie(donnee)
            except:
                rep += self.p_class
        return rep

    def repr_arbre(self, level=0):
        """ Représentation sous forme de string de l'arbre de décision duquel\
            le noeud courant est la racine. 
        """

        rep = ''
        if self.terminal():
            rep += '---'*level
            rep += 'Alors {}\n'.format(self.classe().upper())
            rep += '---'*level
            rep += 'Décision basée sur les données:\n'
            for donnee in self.donnees:
                rep += '---'*level
                rep += str(donnee) + '\n' 

        else:
            for b in [True, False]:
                enfant = self.enfants[b]
                if(b):
                    op = "<="
                else:
                    op = ">"
                rep += '---'*level
                rep += f'Si {self.attribut} {op} {self.seuil}: \n'
                rep += enfant.repr_arbre(level+1)

        return rep

    def __repr__(self):
        """ Représentation sous forme de string de l'arbre de décision duquel\
            le noeud courant est la racine. 
        """

        return str(self.repr_arbre(level=0))

    def get_max_height(self):
        height = 0

        if self.terminal():
            return 0
       
        for enfant in self.enfants.items():
             height = max(height, enfant.get_max_height)
        
        return height + 1
        

    def get_mean_height(self, level=0): 
        total_height = self.get_total_height()
        total_donnee = self.get_total_donnee()
        return total_height/total_donnee
    
    def get_total_donnee(self):
        total = 0
        if self.terminal:
            return len(self.donnees)
        else:
            for enfant in self.enfants.items():
                total+=enfant.get_total_donnee()
        return total

    def get_total_height(self, level=0):
        total = 0
        if self.terminal():
            return len(self.donnees) * level
        else:
            for enfant in self.enfants.items():
                total+= enfant.get_total_height(level+1)
        return total


    def child_num(self):
        total = 0
        if self.terminal():
            return 1
        else:
            for enfant in self.enfants.items():
                total += enfant.child_num
        return total