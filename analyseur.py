from collections import Counter
from typing import Dict


class AnalyseurFrequences:
    """Classe pour analyser les fréquences des caractères dans un texte"""
    
    @staticmethod
    def calculer_frequences(texte: str) -> Dict[str, int]:
        """
        Compte le nombre d'apparitions de chaque caractère.
        
        Args:
            texte: Le texte à analyser
            
        Returns:
            Dictionnaire {caractère: fréquence}
        """
        return dict(Counter(texte))
    
    @staticmethod
    def afficher_caractere(caractere: str) -> str:
        """Retourne une représentation lisible d'un caractère"""
        representations = {
            ' ': '␣ (espace)',
            '\n': '↵ (retour ligne)',
            '\t': '⇥ (tabulation)',
            '\r': '⏎ (retour chariot)'
        }
        return representations.get(caractere, f"'{caractere}'")
    
    @staticmethod
    def get_statistiques(frequences: Dict[str, int]) -> dict:
        """Retourne des statistiques sur les fréquences"""
        total_caracteres = sum(frequences.values())
        nb_uniques = len(frequences)
        
        # Trier par fréquence
        freq_triees = sorted(frequences.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_caracteres': total_caracteres,
            'nb_uniques': nb_uniques,
            'freq_triees': freq_triees,
            'plus_frequent': freq_triees[0] if freq_triees else None,
            'moins_frequent': freq_triees[-1] if freq_triees else None
        }

