

from noeud import NoeudHuffman
from typing import Dict
import os
import subprocess
import platform

class Visualiseur:
    """Classe pour visualiser l'arbre et les données"""
    
    @staticmethod
    def verifier_graphviz():
        """Vérifie si Graphviz est installé"""
        try:
            result = subprocess.run(
                ["dot", "-V"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    @staticmethod
    def generer_graphviz(racine: NoeudHuffman, nom_fichier: str = "arbre_huffman"):
        """
        Génère un fichier DOT ET un PNG pour visualiser l'arbre avec Graphviz.
        
        Args:
            racine: La racine de l'arbre
            nom_fichier: Nom du fichier de sortie (sans extension)
        """
        try:
            dot_content = ["digraph ArbreHuffman {"]
            dot_content.append('    node [shape=circle, style=filled];')
            dot_content.append('    rankdir=TB;')
            
            node_id = [0]  # Compteur pour les IDs uniques
            
            def ajouter_noeud(noeud, parent_id=None, direction=None):
                if noeud is None:
                    return
                
                current_id = node_id[0]
                node_id[0] += 1
                
                # Style du nœud
                if noeud.est_feuille():
                    car = noeud.caractere
                    # Échapper les caractères spéciaux pour Graphviz
                    if car == ' ':
                        car = '␣'
                    elif car == '\n':
                        car = '↵'
                    elif car == '\t':
                        car = '⇥'
                    elif car == '"':
                        car = '\\"'
                    
                    label = f"{car}\\n{noeud.frequence}"
                    color = "lightblue"
                else:
                    label = str(noeud.frequence)
                    color = "lightgray"
                
                dot_content.append(f'    node{current_id} [label="{label}", fillcolor="{color}"];')
                
                # Ajouter l'arête si ce n'est pas la racine
                if parent_id is not None:
                    edge_label = direction
                    dot_content.append(f'    node{parent_id} -> node{current_id} [label="{edge_label}"];')
                
                # Récursion pour les enfants
                if not noeud.est_feuille():
                    ajouter_noeud(noeud.gauche, current_id, "0")
                    ajouter_noeud(noeud.droite, current_id, "1")
            
            ajouter_noeud(racine)
            dot_content.append("}")
            
            # Écrire le fichier DOT
            fichier_dot = f"{nom_fichier}.dot"
            with open(fichier_dot, "w", encoding="utf-8") as f:
                f.write("\n".join(dot_content))
            
            print(f"\n✓ Fichier DOT généré : {fichier_dot}")
            
            # GÉNÉRATION AUTOMATIQUE DU PNG
            if Visualiseur.verifier_graphviz():
                try:
                    fichier_png = f"{nom_fichier}.png"
                    
                    # Générer le PNG avec dot
                    subprocess.run(
                        ["dot", "-Tpng", fichier_dot, "-o", fichier_png],
                        check=True,
                        capture_output=True
                    )
                    
                    print(f"✓ Image PNG générée : {fichier_png}")
                    
                    # Ouvrir automatiquement l'image
                    Visualiseur._ouvrir_image(fichier_png)
                    
                except subprocess.CalledProcessError as e:
                    print(f"❌ Erreur lors de la génération du PNG : {e}")
                    print(f"   Commande manuelle : dot -Tpng {fichier_dot} -o {fichier_png}")
            else:
                print("\n⚠️  Graphviz n'est pas installé !")
                print("   📦 Installation :")
                print("      Windows : https://graphviz.org/download/")
                print("      macOS   : brew install graphviz")
                print("      Linux   : sudo apt install graphviz")
                print(f"\n   🌐 Alternative : https://dreampuf.github.io/GraphvizOnline/")
                print(f"      Ouvrez {fichier_dot} et copiez le contenu")
            
        except Exception as e:
            print(f"⚠️  Erreur lors de la génération : {e}")
    
    @staticmethod
    def _ouvrir_image(fichier_png):
        """Ouvre automatiquement l'image PNG"""
        try:
            systeme = platform.system()
            
            if systeme == "Windows":
                os.startfile(fichier_png)
                print(f"   → Image ouverte automatiquement")
            elif systeme == "Darwin":  # macOS
                subprocess.run(["open", fichier_png], check=True)
                print(f"   → Image ouverte automatiquement")
            else:  # Linux
                subprocess.run(["xdg-open", fichier_png], check=True)
                print(f"   → Image ouverte automatiquement")
                
        except Exception:
            # Si l'ouverture échoue, ce n'est pas grave
            print(f"   📁 Ouvrez manuellement : {fichier_png}")
    
    @staticmethod
    def afficher_arbre_ascii(racine: NoeudHuffman, prefixe: str = "", est_gauche: bool = True):
        """Affiche l'arbre en ASCII art dans la console"""
        if racine is None:
            return
        
        print(prefixe + ("├── " if est_gauche else "└── "), end="")
        
        if racine.est_feuille():
            car = racine.caractere
            if car == ' ':
                car = '␣'
            elif car == '\n':
                car = '↵'
            elif car == '\t':
                car = '⇥'
            print(f"[{car}:{racine.frequence}]")
        else:
            print(f"({racine.frequence})")
        
        # Récursion pour les enfants
        if not racine.est_feuille():
            nouveau_prefixe = prefixe + ("│   " if est_gauche else "    ")
            if racine.gauche:
                Visualiseur.afficher_arbre_ascii(racine.gauche, nouveau_prefixe, True)
            if racine.droite:
                Visualiseur.afficher_arbre_ascii(racine.droite, nouveau_prefixe, False)