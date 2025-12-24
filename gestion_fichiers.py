import pickle
import os
from typing import Tuple, Optional
from huffman import CompressionHuffman
from affichage import Affichage

class GestionFichiers:
    """Classe pour gérer la compression et décompression de fichiers"""
    
    @staticmethod
    def compresser_fichier(fichier_entree: str, fichier_sortie: Optional[str] = None, 
                          afficher_details: bool = True) -> bool:
        """
        Compresse un fichier texte en format Huffman.
        
        Args:
            fichier_entree: Chemin du fichier à compresser
            fichier_sortie: Chemin du fichier compressé (optionnel)
            afficher_details: Afficher les statistiques
            
        Returns:
            True si succès, False sinon
        """
        try:
            # Générer le nom du fichier de sortie si non fourni
            if fichier_sortie is None:
                fichier_sortie = fichier_entree + ".huff"
            
            if afficher_details:
                Affichage.titre("🗜️  COMPRESSION DE FICHIER")
                print(f"\n📄 Fichier d'entrée : {fichier_entree}")
            
            # Lire le fichier
            with open(fichier_entree, 'r', encoding='utf-8') as f:
                texte = f.read()
            
            if afficher_details:
                print(f"✓ Fichier lu : {len(texte)} caractères")
            
            # Compresser
            compression = CompressionHuffman(texte)
            compression.executer(afficher_details=afficher_details)
            
            # Sauvegarder
            GestionFichiers._sauvegarder_compression(
                fichier_sortie, 
                compression.texte_encode,
                compression.racine,
                compression.codes
            )
            
            # Statistiques fichier
            taille_originale = os.path.getsize(fichier_entree)
            taille_compressee = os.path.getsize(fichier_sortie)
            
            if afficher_details:
                Affichage.section("💾 SAUVEGARDE")
                print(f"\n✓ Fichier compressé sauvegardé : {fichier_sortie}")
                print(f"\n{'Métrique':<30} {'Valeur'}")
                print("-" * 70)
                print(f"{'Taille fichier original':<30} {taille_originale:,} octets")
                print(f"{'Taille fichier compressé':<30} {taille_compressee:,} octets")
                print(f"{'Ratio de compression':<30} {(taille_compressee/taille_originale)*100:.2f}%")
                print(f"{'Espace économisé':<30} {taille_originale - taille_compressee:,} octets")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ Erreur : Fichier '{fichier_entree}' introuvable !")
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la compression : {e}")
            return False
    
    @staticmethod
    def decompresser_fichier(fichier_entree: str, fichier_sortie: Optional[str] = None,
                            afficher_details: bool = True) -> bool:
        """
        Décompresse un fichier .huff en fichier texte.
        
        Args:
            fichier_entree: Chemin du fichier .huff
            fichier_sortie: Chemin du fichier décompressé (optionnel)
            afficher_details: Afficher les détails
            
        Returns:
            True si succès, False sinon
        """
        try:
            # Générer le nom du fichier de sortie
            if fichier_sortie is None:
                if fichier_entree.endswith('.huff'):
                    fichier_sortie = fichier_entree[:-5] + ".decompresse.txt"
                else:
                    fichier_sortie = fichier_entree + ".decompresse.txt"
            
            if afficher_details:
                Affichage.titre("🔓 DÉCOMPRESSION DE FICHIER")
                print(f"\n📄 Fichier compressé : {fichier_entree}")
            
            # Charger les données
            texte_encode, racine, codes = GestionFichiers._charger_compression(fichier_entree)
            
            if afficher_details:
                print(f"✓ Données chargées")
                print(f"  - Bits encodés : {len(texte_encode)}")
                print(f"  - Codes dans le dictionnaire : {len(codes)}")
            
            # Décoder
            from encodeur import Encodeur
            texte_decode = Encodeur.decoder(texte_encode, racine)
            
            # Sauvegarder
            with open(fichier_sortie, 'w', encoding='utf-8') as f:
                f.write(texte_decode)
            
            if afficher_details:
                Affichage.section("💾 DÉCOMPRESSION RÉUSSIE")
                print(f"\n✓ Fichier décompressé sauvegardé : {fichier_sortie}")
                print(f"  Caractères restaurés : {len(texte_decode)}")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ Erreur : Fichier '{fichier_entree}' introuvable !")
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la décompression : {e}")
            return False
    
    @staticmethod
    def _sauvegarder_compression(fichier: str, texte_encode: str, racine, codes: dict):
        """Sauvegarde les données de compression dans un fichier"""
        donnees = {
            'texte_encode': texte_encode,
            'racine': racine,
            'codes': codes,
            'version': '1.0'
        }
        
        with open(fichier, 'wb') as f:
            pickle.dump(donnees, f)
    
    @staticmethod
    def _charger_compression(fichier: str) -> Tuple[str, any, dict]:
        """Charge les données de compression depuis un fichier"""
        with open(fichier, 'rb') as f:
            donnees = pickle.load(f)
        
        return donnees['texte_encode'], donnees['racine'], donnees['codes']
    
    @staticmethod
    def comparer_fichiers(fichier_original: str, fichier_decompresse: str) -> bool:
        """Compare deux fichiers pour vérifier l'intégrité"""
        try:
            with open(fichier_original, 'r', encoding='utf-8') as f1:
                contenu1 = f1.read()
            
            with open(fichier_decompresse, 'r', encoding='utf-8') as f2:
                contenu2 = f2.read()
            
            return contenu1 == contenu2
            
        except Exception as e:
            print(f"❌ Erreur lors de la comparaison : {e}")
            return False
    
    @staticmethod
    def tester_sur_fichier(fichier: str):
        """
        Test complet : compression + décompression + vérification
        C'est la fonction principale pour "Tester sur un fichier"
        """
        Affichage.titre("🧪 TEST COMPLET SUR FICHIER")
        print(f"\n📝 Fichier de test : {fichier}")
        
        # Vérifier que le fichier existe
        if not os.path.exists(fichier):
            print(f"❌ Le fichier '{fichier}' n'existe pas !")
            return False
        
        # 1. Compression
        print("\n" + "="*70)
        print("ÉTAPE 1 : COMPRESSION".center(70))
        print("="*70)
        
        fichier_compresse = fichier + ".huff"
        succes = GestionFichiers.compresser_fichier(
            fichier, 
            fichier_compresse, 
            afficher_details=True
        )
        
        if not succes:
            return False
        
        # 2. Décompression
        print("\n" + "="*70)
        print("ÉTAPE 2 : DÉCOMPRESSION".center(70))
        print("="*70)
        
        fichier_decompresse = fichier + ".decompresse.txt"
        succes = GestionFichiers.decompresser_fichier(
            fichier_compresse,
            fichier_decompresse,
            afficher_details=True
        )
        
        if not succes:
            return False
        
        # 3. Vérification
        print("\n" + "="*70)
        print("ÉTAPE 3 : VÉRIFICATION".center(70))
        print("="*70)
        
        identique = GestionFichiers.comparer_fichiers(fichier, fichier_decompresse)
        
        if identique:
            print("\n✅ SUCCÈS TOTAL !")
            print("   ✓ Compression réussie")
            print("   ✓ Décompression réussie")
            print("   ✓ Fichier original et décompressé sont identiques")
            print(f"\n📊 Fichiers créés :")
            print(f"   - Compressé   : {fichier_compresse}")
            print(f"   - Décompressé : {fichier_decompresse}")
        else:
            print("\n❌ ERREUR : Les fichiers sont différents !")
            return False
        
        return True
    
    @staticmethod
    def lister_fichiers_texte(dossier: str = ".") -> list:
        """Liste tous les fichiers .txt dans un dossier"""
        fichiers = []
        try:
            for fichier in os.listdir(dossier):
                if fichier.endswith('.txt') and not fichier.endswith('.decompresse.txt'):
                    fichiers.append(os.path.join(dossier, fichier))
        except Exception as e:
            print(f"Erreur : {e}")
        
        return fichiers
    
    @staticmethod
    def nettoyer_fichiers_temporaires(fichier_base: str):
        """Supprime les fichiers temporaires créés lors des tests"""
        fichiers_a_supprimer = [
            fichier_base + ".huff",
            fichier_base + ".decompresse.txt"
        ]
        
        for fichier in fichiers_a_supprimer:
            try:
                if os.path.exists(fichier):
                    os.remove(fichier)
                    print(f"✓ Supprimé : {fichier}")
            except Exception as e:
                print(f"⚠️  Impossible de supprimer {fichier} : {e}")
