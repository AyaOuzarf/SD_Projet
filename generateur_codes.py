from typing import Dict
from noeud import NoeudHuffman

class GenerateurCodes:
    """Classe pour générer les codes de Huffman"""
    
    @staticmethod
    def generer(racine: NoeudHuffman) -> Dict[str, str]:
        """
        associer un code binaire à chaque caractère.

        
        Args:
            racine: La racine de l'arbre de Huffman
            
        Returns:
            Dictionnaire {caractère: code_binaire}
        """
        codes = {}
        
        def parcourir(noeud: NoeudHuffman, code_actuel: str):
            if noeud is None:
                return
            
            # Si c'est une feuille, on a trouvé un caractère
            if noeud.est_feuille():
                codes[noeud.caractere] = code_actuel if code_actuel else '0'
                return
            
            # Sinon, continuer le parcours
            #aller à gauche ajoute 0 au code,
            #aller à droite ajoute 1 au code,
            parcourir(noeud.gauche, code_actuel + '0')
            parcourir(noeud.droite, code_actuel + '1')
        
        parcourir(racine, '')
        return codes
    
    @staticmethod
    def calculer_longueur_moyenne(codes: Dict[str, str], frequences: Dict[str, int]) -> float:
        """Calcule la longueur moyenne des codes pondérée par les fréquences"""
        total_bits = sum(len(code) * frequences[car] for car, code in codes.items())
        total_caracteres = sum(frequences.values())
        return total_bits / total_caracteres if total_caracteres > 0 else 0
