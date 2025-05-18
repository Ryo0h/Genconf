# genconf.py
# Script de génération de fichiers de configuration réseau à partir de templates Jinja2
# et de données sources JSON/CSV. Produit un fichier de configuration par type.

from jinja2 import Environment, FileSystemLoader
import pandas as pd
import json
import os

# Définir les chemins pour les templates, les données sources et les fichiers de sortie
template_path = 'templates'
data_path = 'data'
output_path = "output"

# Liste des templates à utiliser avec un champ pour stocker leur contenu rendu
template_list = [{'name': 'L2_cisco_config', 'content':""},
                 {'name': 'aaa', 'content':""},
                 {'name': 'iface', 'content':""},
                 {'name': 'tacacs', 'content':""},
                 {'name': 'svi', 'content':""},
                 {'name': 'vlan', 'content':""}]

# Liste pour stocker les rendus finaux (nom, contenu)
render_list = []

# Initialiser l'environnement Jinja2 avec le dossier de templates
env = Environment(loader=FileSystemLoader(template_path))

# Chargement des fichiers de données (JSON pour la config générale, CSV pour VLANs et interfaces)
with open(f'{data_path}/global_config.json','r') as json_file:
    global_config = json.load(json_file)

with open(f'{data_path}/banner_login.txt','r') as f:
    banner_login = f.read()

with open(f'{data_path}/banner_exec.txt','r') as f:
    banner_exec = f.read()

# Charger et convertir les VLANs en liste de dictionnaires
vlan_list = pd.read_csv(f'{data_path}/vlan.csv',keep_default_na=False)
vlan_list = vlan_list.to_dict(orient='records')

# Charger et convertir les interfaces en liste de dictionnaires
iface_list = pd.read_csv(f'{data_path}/iface.csv',keep_default_na=False)
iface_list = iface_list.to_dict(orient='records')

# Pour chaque template, charger le fichier Jinja2 correspondant et le rendre avec les données
for template in template_list:
    template['content']= env.get_template(f"{template['name']}.j2")
    # Ajouter le résultat du rendu dans la liste avec le nom du template
    render_list.append((template['name'],template['content'].render(vlan_list=vlan_list, global_config=global_config, iface_list=iface_list, banner_login=banner_login, banner_exec=banner_exec)))

# Créer les dossiers de sortie s'ils n'existent pas encore
if not os.path.isdir(output_path):
    os.mkdir(output_path)
if not os.path.isdir(f"{output_path}/{global_config['switch']['hostname']}"):
    os.mkdir(f"{output_path}/{global_config['switch']['hostname']}")

# Écrire chaque configuration rendue dans un fichier distinct
for ouput in render_list:
    with open(f"{output_path}/{global_config['switch']['hostname']}/{global_config['switch']['hostname']}_{ouput[0]}.conf",'w') as f:
        f.write(ouput[1])

print("Generated successfully.")