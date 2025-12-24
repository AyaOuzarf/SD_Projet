from typing import Dict, Tuple

class Statistiques:
    """Classe pour calculer et formater les statistiques de compression"""
    
    @staticmethod
    def calculer_compression(texte_original: str, texte_encode: str) -> dict:
        """
        Calcule les statistiques de compression.
        
        Returns:
            Dictionnaire avec toutes les statistiques
        """
        taille_originale = len(texte_original) * 8
        taille_compressee = len(texte_encode)
        
        taux_compression = taille_compressee / taille_originale if taille_originale > 0 else 0
        gain = 1 - taux_compression
        facteur = taille_originale / taille_compressee if taille_compressee > 0 else 0
        bits_economises = taille_originale - taille_compressee
        
        return {
            'taille_originale_bits': taille_originale,
            'taille_originale_octets': taille_originale // 8,
            'taille_compressee_bits': taille_compressee,
            'taille_compressee_octets': taille_compressee // 8,
            'bits_economises': bits_economises,
            'taux_compression': taux_compression,
            'gain': gain,
            'facteur_compression': facteur
        }
    
    @staticmethod
    def formater_taille(bits: int) -> str:
        """Formate une taille en bits de manière lisible"""
        octets = bits / 8
        if octets < 1024:
            return f"{octets:.2f} octets"
        elif octets < 1024 * 1024:
            return f"{octets/1024:.2f} Ko"
        else:
            return f"{octets/(1024*1024):.2f} Mo"

