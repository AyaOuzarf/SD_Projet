from typing import Dict
from noeud import NoeudHuffman

class Encodeur:
    """Classe pour encoder et décoder le texte"""
    
    @staticmethod
    def encoder(texte: str, codes: Dict[str, str]) -> str:
        """
        Encode le texte en utilisant les codes de Huffman.
        
        Args:
            texte: Le texte à encoder
            codes: Dictionnaire {caractère: code_binaire}
            
        Returns:
            Le texte encodé (chaîne de 0 et 1)
        """
        return ''.join(codes[caractere] for caractere in texte)
    
    @staticmethod
    def decoder(texte_encode: str, racine: NoeudHuffman) -> str:
        """
        Décode un texte encodé en utilisant l'arbre de Huffman.
        
        Args:
            texte_encode: Chaîne de bits (0 et 1)
            racine: La racine de l'arbre de Huffman
            
        Returns:
            Le texte décodé
        """
        if not texte_encode:
            return ""
        
        texte_decode = []
        noeud_actuel = racine
        
        for bit in texte_encode:
            # Se déplacer dans l'arbre selon le bit
            if bit == '0':
                noeud_actuel = noeud_actuel.gauche
            else:
                noeud_actuel = noeud_actuel.droite
            
            # Si on atteint une feuille, on a trouvé un caractère
            if noeud_actuel.est_feuille():
                texte_decode.append(noeud_actuel.caractere)
                noeud_actuel = racine
        
        return ''.join(texte_decode)
