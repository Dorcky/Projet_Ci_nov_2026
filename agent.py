import os
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    print(f"Exécution : {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"La commande a échoué avec le code {result.returncode}")
    return result

def main():
    target_dir = Path(r"G:\bois_boulogne\projet_synthese\github_action")
    print(f"Création et configuration du projet dans : {target_dir}")

    # Étape 1 : Création de l'arborescence des dossiers
    workflows_dir = target_dir / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    print("Dossiers créés avec succès.")

    # Étape 2 : Création du fichier main.py
    main_py_path = target_dir / "main.py"
    main_content = """with open('sortie.txt', 'a') as fout:
    print('Bienvenue initial')
    fout.write('Ligne 1: Bienvenue Monde')
"""
    main_py_path.write_text(main_content, encoding="utf-8")
    print("Fichier main.py créé.")

    # Étape 3 : Création du fichier de workflow cml.yaml
    cml_yaml_path = workflows_dir / "cml.yaml"
    cml_content = """name: pratique CICD
on: [push]
jobs:
  run:
    runs-on: [ubuntu-latest]
    steps:
      - name: Set up Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - uses: actions/checkout@v3
      - name: cml_run
        env:
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          ACTIONS_RUNNER_FORCE_ACTIONS_NODE_VERSION: node16
          ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION: 'true'
        run: |
          # Workflow goes here
           
          python main.py
          # Write your CML report
          echo "## Message:" >> report.md
          cat sortie.txt >> report.md
         
          #cml-send-comment metrics.txt 
          #cml-send-comment report.md
          git config --global user.email "mhafod@yahoo.com"
          git config --global user.name "degenio"
          git add report.md sortie.txt
          git commit -m "pousser vers github repository"
          git push origin HEAD:main
"""
    cml_yaml_path.write_text(cml_content, encoding="utf-8")
    print("Fichier cml.yaml créé.")

    # Étape 4 : Initialisation du dépôt Git local et commit initial
    if not (target_dir / ".git").exists():
        run_command("git init", cwd=target_dir)
    
    run_command("git add .", cwd=target_dir)
    
    # Configuration locale git si nécessaire pour éviter les erreurs de commit
    run_command('git config user.email "mhafod@yahoo.com"', cwd=target_dir)
    run_command('git config user.name "degenio"', cwd=target_dir)
    
    # Vérifier s'il y a des éléments à commiter
    status_res = run_command("git status --porcelain", cwd=target_dir)
    if status_res.stdout.strip():
        run_command('git commit -m "push initial avec workflow CML et main.py"', cwd=target_dir)
        print("Commit initial effectué avec succès.")
    else:
        print("Aucun changement à commiter (déjà à jour).")

    print("\n--- Bilan ---")
    print(f"Le projet a été entièrement préparé dans : {target_dir}")
    print("Prochaines étapes recommandées :")
    print("1. Ouvrir GitHub Desktop ou votre terminal pour publier le dépôt sur GitHub.")
    print("2. Configurer les permissions de workflow dans GitHub (Settings > Actions > General > Read and write permissions).")

if __name__ == "__main__":
    main()