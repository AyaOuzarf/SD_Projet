"""
main.py - Version Corrigée
Demande si l'utilisateur veut générer le graphique PNG
"""

from huffman import CompressionHuffman
from affichage import Affichage
from gestion_fichiers import GestionFichiers
from visualiseur import Visualiseur
import os

def demander_generation_graphique(compression, nom_fichier="arbre_huffman"):
    """
    Demande à l'utilisateur s'il veut générer le graphique
    
    Args:
        compression: Instance de CompressionHuffman
        nom_fichier: Nom du fichier de sortie
    """
    print("\n" + "="*70)
    choix = input("🎨 Voulez-vous générer l'arbre graphique (PNG) ? (o/n) : ").strip().lower()
    
    if choix in ['o', 'oui', 'y', 'yes']:
        print("\n🎨 Génération du graphique...")
        Visualiseur.generer_graphviz(compression.racine, nom_fichier=nom_fichier)
    else:
        print("   ⏩ Génération du graphique ignorée")

def exemple1_phrase_simple():
    """Exemple avec la phrase du cours"""
    print("\n" + "🎯 EXEMPLE 1 : Phrase du cours".center(70, "="))
    
    texte = "je veux et j'exige d'exquises excuses"
    print(f"\nTexte : \"{texte}\"")
    
    # Compression
    compression = CompressionHuffman(texte)
    compression.executer(afficher_details=True)
    
    # Affichage ASCII
    compression.visualiser_arbre("ascii")
    
    # Vérification
    Affichage.section("✅ VÉRIFICATION")
    if compression.verifier():
        print("✓ Compression et décompression réussies !")
    
    # Demander si on génère le PNG
    demander_generation_graphique(compression, nom_fichier="arbre_huffman_exemple1")

def exemple2_texte_long():
    """Exemple avec un texte plus long"""
    print("\n" + "🎯 EXEMPLE 2 : Texte long".center(70, "="))
    
    texte = """Le codage de Huffman est une méthode de compression de données.
Cette technique utilise un arbre binaire pour représenter les caractères.
Les caractères les plus fréquents ont des codes plus courts.
Cela permet d'économiser de l'espace de stockage."""
    
    # Compression
    compression = CompressionHuffman(texte)
    compression.executer(afficher_details=True)
    
    # Affichage ASCII
    compression.visualiser_arbre("ascii")
    
    # Vérification
    if compression.verifier():
        print("\n✓ Vérification OK !")
    
    # Demander si on génère le PNG
    demander_generation_graphique(compression, nom_fichier="arbre_huffman_exemple2")

def exemple3_comparaison():
    """Compare différents types de textes"""
    print("\n" + "🎯 EXEMPLE 3 : Comparaison".center(70, "="))
    
    textes = {
        "Répétitif": "aaaaaaabbbbcccdde",
        "Varié": "abcdefghijklmnop",
        "Français": "Bonjour le monde !",
        "Code": "def hello(): print('Hello')"
    }
    
    print(f"\n{'Type':<15} {'Taux':<12} {'Gain':<12} {'Facteur'}")
    print("-" * 70)
    
    for nom, texte in textes.items():
        c = CompressionHuffman(texte)
        c.executer(afficher_details=False)
        s = c.statistiques
        print(f"{nom:<15} {s['taux_compression']:<11.2%} {s['gain']:<11.2%} {s['facteur_compression']:.2f}x")
    
    # Demander si on veut visualiser un des arbres
    print("\n" + "="*70)
    choix_visu = input("Voulez-vous visualiser un des arbres ? (tapez le numéro ou 'n') : ").strip()
    
    if choix_visu.isdigit() and 1 <= int(choix_visu) <= len(textes):
        texte_choisi = list(textes.values())[int(choix_visu) - 1]
        nom_choisi = list(textes.keys())[int(choix_visu) - 1]
        
        print(f"\n🌳 Génération de l'arbre pour : {nom_choisi}")
        c = CompressionHuffman(texte_choisi)
        c.executer(afficher_details=False)
        c.visualiser_arbre("ascii")
        
        demander_generation_graphique(c, nom_fichier=f"arbre_huffman_comparaison_{nom_choisi.lower()}")

def exemple4_test_fichier():
    """Test complet sur un fichier"""
    print("\n" + "🎯 EXEMPLE 4 : Test sur fichier".center(70, "="))
    
    # Créer un fichier de test s'il n'existe pas
    fichier_test = "exemples/test_compression.txt"
    
    if not os.path.exists(fichier_test):
        print(f"\n📝 Création du fichier de test : {fichier_test}")
        os.makedirs("exemples", exist_ok=True)
        with open(fichier_test, 'w', encoding='utf-8') as f:
            f.write("""Le codage de Huffman a été développé par David A. Huffman en 1952.
C'est un algorithme de compression sans perte très efficace.
Il est utilisé dans de nombreux formats de compression modernes.
ZIP, JPEG, MP3 utilisent tous des variantes de l'algorithme de Huffman.
La compression fonctionne en assignant des codes plus courts aux caractères fréquents.
Les caractères rares reçoivent des codes plus longs.
Cela optimise l'espace de stockage nécessaire.""")
        print("✓ Fichier créé")
    
    # Tester
    GestionFichiers.tester_sur_fichier(fichier_test)
    
    # Proposer de visualiser l'arbre
    print("\n" + "="*70)
    choix = input("🎨 Voulez-vous visualiser l'arbre de ce fichier ? (o/n) : ").strip().lower()
    
    if choix in ['o', 'oui', 'y', 'yes']:
        with open(fichier_test, 'r', encoding='utf-8') as f:
            texte = f.read()
        
        compression = CompressionHuffman(texte)
        compression.executer(afficher_details=False)
        
        print("\n🌳 Arbre ASCII :")
        compression.visualiser_arbre("ascii")
        
        print("\n" + "="*70)
        choix_png = input("🎨 Générer aussi le graphique PNG ? (o/n) : ").strip().lower()
        
        if choix_png in ['o', 'oui', 'y', 'yes']:
            Visualiseur.generer_graphviz(compression.racine, nom_fichier="arbre_huffman_fichier_test")

def menu_gestion_fichiers():
    """Sous-menu pour la gestion de fichiers"""
    while True:
        print("\n" + "="*70)
        print("📁 GESTION DE FICHIERS".center(70))
        print("="*70)
        print("1. Compresser un fichier")
        print("2. Décompresser un fichier")
        print("3. Test complet (compression + décompression + vérification)")
        print("4. Lister les fichiers .txt disponibles")
        print("0. Retour au menu principal")
        print("="*70)
        
        choix = input("\nChoix : ").strip()
        
        if choix == "0":
            break
        elif choix == "1":
            fichier = input("\nFichier à compresser : ").strip()
            if fichier and os.path.exists(fichier):
                GestionFichiers.compresser_fichier(fichier)
            else:
                print("❌ Fichier introuvable !")
        
        elif choix == "2":
            fichier = input("\nFichier .huff à décompresser : ").strip()
            if fichier and os.path.exists(fichier):
                GestionFichiers.decompresser_fichier(fichier)
            else:
                print("❌ Fichier introuvable !")
        
        elif choix == "3":
            fichier = input("\nFichier à tester : ").strip()
            if fichier and os.path.exists(fichier):
                GestionFichiers.tester_sur_fichier(fichier)
            else:
                print("❌ Fichier introuvable !")
        
        elif choix == "4":
            dossier = input("\nDossier (ou . pour actuel) : ").strip() or "."
            fichiers = GestionFichiers.lister_fichiers_texte(dossier)
            
            if fichiers:
                print(f"\n📄 Fichiers .txt trouvés dans '{dossier}' :")
                for i, f in enumerate(fichiers, 1):
                    taille = os.path.getsize(f)
                    print(f"  {i}. {f} ({taille} octets)")
            else:
                print("Aucun fichier .txt trouvé")

def menu_principal():
    """Menu principal interactif"""
    Affichage.titre("🎮 MENU - CODAGE DE HUFFMAN")
    
    while True:
        print("\n" + "="*70)
        print("OPTIONS :".center(70))
        print("="*70)
        print("  1. Exemple : Phrase du cours")
        print("  2. Exemple : Texte long")
        print("  3. Comparaison de textes")
        print("  4. Test complet sur fichier (REQUIS)")
        print("  5. Gestion de fichiers")
        print("  6. Entrer votre propre texte")
        print("  0. Quitter")
        print("="*70)
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "0":
            print("\n👋 Au revoir !")
            break
        elif choix == "1":
            exemple1_phrase_simple()
        elif choix == "2":
            exemple2_texte_long()
        elif choix == "3":
            exemple3_comparaison()
        elif choix == "4":
            exemple4_test_fichier()
        elif choix == "5":
            menu_gestion_fichiers()
        elif choix == "6":
            texte = input("\nEntrez votre texte : ")
            if texte:
                print("\n🔄 Compression en cours...")
                c = CompressionHuffman(texte)
                c.executer()
                
                # Affichage ASCII
                print("\n🌳 Arbre ASCII :")
                c.visualiser_arbre("ascii")
                
                # Vérification
                if c.verifier():
                    print("\n✓ Vérification OK !")
                
                # Demander génération PNG
                demander_generation_graphique(c, nom_fichier="arbre_huffman_texte_perso")
        else:
            print("⚠️  Choix invalide !")

if __name__ == "__main__":
    menu_principal()