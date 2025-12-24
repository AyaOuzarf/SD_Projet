class NoeudHuffman:
    """
    Représente un nœud dans l'arbre de Huffman.
    
    Attributs:
        caractere: Le caractère stocké (None pour les nœuds internes)
        frequence: La fréquence d'apparition
        gauche: Enfant gauche (pour code 0)
        droite: Enfant droit (pour code 1)
    """
    
    def __init__(self, caractere=None, frequence=0):
        self.caractere = caractere
        self.frequence = frequence
        self.gauche = None
        self.droite = None
    
    def __lt__(self, autre):
        """Comparaison pour le heap (file de priorité)"""
        return self.frequence < autre.frequence
    
    def __eq__(self, autre):
        return self.frequence == autre.frequence
    
    def est_feuille(self):
        """Vérifie si le nœud est une feuille (contient un caractère)"""
        return self.gauche is None and self.droite is None
    
    def __repr__(self):
        if self.caractere:
            return f"NoeudHuffman('{self.caractere}', {self.frequence})"
        return f"NoeudHuffman(interne, {self.frequence})"

