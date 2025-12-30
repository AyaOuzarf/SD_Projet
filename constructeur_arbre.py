import heapq
from typing import Dict
from noeud import NoeudHuffman

class ConstructeurArbre:
    """Classe pour construire l'arbre de Huffman"""
    
    @staticmethod
    def construire(frequences: Dict[str, int]) -> NoeudHuffman:
        """
        Construit l'arbre de Huffman à partir des fréquences.
        
        Args:
            frequences: Dictionnaire {caractère: fréquence}
            
        Returns:
            La racine de l'arbre de Huffman
        """
        
        # Cas spécial : un seul caractère
        if len(frequences) == 1:
            caractere, freq = list(frequences.items())[0]
            racine = NoeudHuffman(None, freq)
            racine.gauche = NoeudHuffman(caractere, freq)
            return racine
        
        # Créer un min-heap (sélectionner les deux caractères ayant les plus petites fréquences)
        heap = []
        for caractere, freq in frequences.items():
            noeud = NoeudHuffman(caractere, freq)
            heapq.heappush(heap, noeud)
        
        historique = []
        iteration = 1
        
        # Fusionner les nœuds jusqu'à n'en avoir qu'un(fusionnés dans un nouveau nœud parent dont la fréquence est la somme des deux)
        while len(heap) > 1:
            # Extraire les 2 nœuds de plus petite fréquence
            gauche = heapq.heappop(heap)
            droite = heapq.heappop(heap)
            
            # Créer un nouveau nœud parent
            parent = NoeudHuffman(None, gauche.frequence + droite.frequence)
            parent.gauche = gauche
            parent.droite = droite
            
            # Réinsérer le parent
            heapq.heappush(heap, parent)
            
            historique.append({
                'iteration': iteration,
                'gauche_freq': gauche.frequence,
                'droite_freq': droite.frequence,
                'parent_freq': parent.frequence
            })
            iteration += 1
        
        racine = heap[0]
        racine.historique = historique
        return racine
