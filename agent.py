import os
from pathlib import Path

def main():
    target_dir = Path(r"G:\bois_boulogne\projet_synthese\github_action")
    gitignore_path = target_dir / ".gitignore"
    
    print(f"Mise à jour du fichier .gitignore dans : {target_dir}")

    # Lecture du contenu existant de .gitignore s'il existe
    existing_content = ""
    if gitignore_path.exists():
        existing_content = gitignore_path.read_text(encoding="utf-8")

    # Vérifier si agent.py est déjà présent dans le .gitignore
    target_line = "agent.py"
    lines = [line.strip() for line in existing_content.splitlines()]

    if target_line in lines:
        print("Le fichier agent.py est déjà présent dans le .gitignore.")
    else:
        # Ajouter agent.py proprement
        with open(gitignore_path, "a", encoding="utf-8") as f:
            if existing_content and not existing_content.endswith("\n"):
                f.write("\n")
            f.write("# Ignorer les scripts de l'agent local\n")
            f.write("agent.py\n")
        print("agent.py a été ajouté avec succès au fichier .gitignore.")

    print("\n--- Bilan ---")
    print("Le fichier .gitignore a été mis à jour.")
    print("Prochaine étape : Vous pouvez maintenant commiter et pousser cette modification via GitHub Desktop ou votre terminal.")

if __name__ == "__main__":
    main()