from typing import Dict
from analyseur import AnalyseurFrequences
from statistiques import Statistiques

class Affichage:
    """Classe pour afficher les résultats de manière formatée"""
    
    LARGEUR = 70
    
    @staticmethod
    def titre(texte: str):
        """Affiche un titre encadré"""
        print("\n" + "=" * Affichage.LARGEUR)
        print(texte.center(Affichage.LARGEUR))
        print("=" * Affichage.LARGEUR)
    
    @staticmethod
    def section(texte: str):
        """Affiche un titre de section"""
        print(f"\n{texte}")
        print("-" * Affichage.LARGEUR)
    
    @staticmethod
    def frequences(frequences: Dict[str, int]):
        """Affiche les fréquences des caractères"""
        Affichage.section("📊 ANALYSE DES FRÉQUENCES")
        
        stats = AnalyseurFrequences.get_statistiques(frequences)
        
        print(f"\n{'Caractère':<20} {'Fréquence':<12} {'Pourcentage'}")
        print("-" * Affichage.LARGEUR)
        
        for caractere, freq in stats['freq_triees'][:10]:  # Top 10
            affichage = AnalyseurFrequences.afficher_caractere(caractere)
            pourcentage = (freq / stats['total_caracteres']) * 100
            print(f"{affichage:<20} {freq:<12} {pourcentage:>6.2f}%")
        
        if len(stats['freq_triees']) > 10:
            print(f"... et {len(stats['freq_triees']) - 10} autres caractères")
        
        print(f"\n✓ Total : {stats['total_caracteres']} caractères ({stats['nb_uniques']} uniques)")
    
    @staticmethod
    def codes(codes: Dict[str, str], frequences: Dict[str, int]):
        """Affiche la table des codes de Huffman"""
        Affichage.section("💻 TABLE DES CODES DE HUFFMAN")
        
        print(f"\n{'Caractère':<15} {'Fréquence':<12} {'Code':<25} {'Bits sauvés'}")
        print("-" * Affichage.LARGEUR)
        
        codes_tries = sorted(codes.items(), key=lambda x: len(x[1]))
        
        for caractere, code in codes_tries:
            affichage = AnalyseurFrequences.afficher_caractere(caractere)
            freq = frequences[caractere]
            economie = (8 - len(code)) * freq
            
            print(f"{affichage:<15} {freq:<12} {code:<25} {economie:+d}")
    
    @staticmethod
    def statistiques(stats: dict):
        """Affiche les statistiques de compression"""
        Affichage.section("📈 STATISTIQUES DE COMPRESSION")
        
        print(f"\n{'Métrique':<30} {'Valeur'}")
        print("-" * Affichage.LARGEUR)
        print(f"{'Taille originale':<30} {stats['taille_originale_bits']:,} bits ({stats['taille_originale_octets']:,} octets)")
        print(f"{'Taille compressée':<30} {stats['taille_compressee_bits']:,} bits ({stats['taille_compressee_octets']:,} octets)")
        print(f"{'Bits économisés':<30} {stats['bits_economises']:,} bits")
        print(f"\n{'Taux de compression':<30} {stats['taux_compression']:.2%}")
        print(f"{'Gain (économie)':<30} {stats['gain']:.2%}")
        print(f"{'Facteur de compression':<30} {stats['facteur_compression']:.2f}x")
    
    @staticmethod
    def construction_arbre(historique: list):
        """Affiche l'historique de construction de l'arbre"""
        Affichage.section("🌳 CONSTRUCTION DE L'ARBRE")
        
        print(f"\nNombre d'itérations : {len(historique)}")
        print(f"\n{'Itération':<12} {'Fusion':<30} {'Résultat'}")
        print("-" * Affichage.LARGEUR)
        
        for etape in historique[:5]:  # Afficher les 5 premières
            fusion = f"{etape['gauche_freq']} + {etape['droite_freq']}"
            print(f"{etape['iteration']:<12} {fusion:<30} {etape['parent_freq']}")
        
        if len(historique) > 5:
            print(f"... et {len(historique) - 5} autres itérations")
