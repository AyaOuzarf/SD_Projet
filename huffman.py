from analyseur import AnalyseurFrequences
from constructeur_arbre import ConstructeurArbre
from generateur_codes import GenerateurCodes
from encodeur import Encodeur
from statistiques import Statistiques
from visualiseur import Visualiseur
from affichage import Affichage

class CompressionHuffman:
    """Classe principale pour la compression Huffman"""
    
    def __init__(self, texte: str):
        self.texte_original = texte
        self.frequences = None
        self.racine = None
        self.codes = None
        self.texte_encode = None
        self.statistiques = None
    
    def executer(self, afficher_details: bool = True):
        """Exécute tout le processus de compression"""
        
        if afficher_details:
            Affichage.titre("🗜️  COMPRESSION HUFFMAN")
        
        # 1. Analyser les fréquences
        self.frequences = AnalyseurFrequences.calculer_frequences(self.texte_original)
        if afficher_details:
            Affichage.frequences(self.frequences)
        
        # 2. Construire l'arbre
        self.racine = ConstructeurArbre.construire(self.frequences)
        if afficher_details and hasattr(self.racine, 'historique'):
            Affichage.construction_arbre(self.racine.historique)
        
        # 3. Générer les codes
        self.codes = GenerateurCodes.generer(self.racine)
        if afficher_details:
            Affichage.codes(self.codes, self.frequences)
        
        # 4. Encoder
        self.texte_encode = Encodeur.encoder(self.texte_original, self.codes)
        
        # 5. Calculer les statistiques
        self.statistiques = Statistiques.calculer_compression(
            self.texte_original, 
            self.texte_encode
        )
        
        if afficher_details:
            Affichage.statistiques(self.statistiques)
        
        return self
    
    def decoder(self) -> str:
        """Décode le texte compressé"""
        return Encodeur.decoder(self.texte_encode, self.racine)
    
    def verifier(self) -> bool:
        """Vérifie que la compression/décompression fonctionne"""
        texte_decode = self.decoder()
        return texte_decode == self.texte_original
    
    def visualiser_arbre(self, format: str = "ascii"):
        """Visualise l'arbre de Huffman"""
        if format == "ascii":
            Affichage.section("🌳 ARBRE DE HUFFMAN (ASCII)")
            print()
            Visualiseur.afficher_arbre_ascii(self.racine, "", True)
        elif format == "graphviz":
            Visualiseur.generer_graphviz(self.racine)
    
    def get_rapport(self) -> dict:
        """Retourne un rapport complet"""
        return {
            'texte_original': self.texte_original,
            'frequences': self.frequences,
            'codes': self.codes,
            'texte_encode': self.texte_encode,
            'statistiques': self.statistiques,
            'verification': self.verifier()
        }

