

# Genconf - Génération de configurations réseau Cisco

## 🔍 Description
Ce projet permet de générer automatiquement des fichiers de configuration Cisco à partir de templates Jinja2 et de fichiers de données (JSON/CSV). Il s'adresse à des administrateurs réseau souhaitant industrialiser la production de configurations réseau L2/L3.

---

## 📁 Arborescence du projet

```
Genconf/
├── data/                # Données sources (CSV, JSON, bannières)
│   ├── global_config.json
│   ├── vlan.csv
│   ├── iface.csv
│   ├── banner_login.txt
│   └── banner_exec.txt
│
├── templates/          # Templates Jinja2 (1 fichier par bloc de config)
│   ├── L2_cisco_config.j2
│   ├── iface.j2
│   ├── svi.j2
│   └── ...
│
├── output/             # Dossier où seront générés les fichiers .conf
│
├── genconf.py          # Script principal
└── README.md           # Ce fichier
```

---

## 📄 Format des fichiers de données

### `global_config.json`
Contient les paramètres globaux du switch (hostname, VTP, TACACS, bannières, etc).

```json
{
  "switch": {
    "hostname": "sw-core"
  },
  "vtp": {
    "mode": "server",
    "domain": "corp",
    "version": "2"
  },
  "tacacs_enable": true,
  "dhcp_relay": ["5.5.5.5", "6.6.6.6"]
}
```
Les paramètres venant en premier (clef "switch") sont les plus susceptibles de changer d'un switch à l'autre. Les autres restent souvent les mêmes au sein d'une même organisation (configuration Tacacs+, radus, comptes locaux, etc)
Modifier directement les valeurs  dans le fichier. 
⚠️ : Il n'y a pas (pour le moment) de vérification des données (adresses IP valides, paramètre IOS précis...)

### `vlan.csv`
Contient les informations sur les VLANs :

```
id,name,layer,ip,mask,vrf,dhcp,acl,direction
10,Management,l3,192.168.10.1,255.255.255.0,mgmt,True,,
20,Users,l2,,,,,,
```
Si une donnée n'est pas nécessaire, par exemple si un vlan n'appartient pas à une VRF ou s'il n'y a pas d'ACL associée, laisser le champs totalement vide.

### `iface.csv`
Contient les interfaces physiques ou logiques :

```
name,description,mode,access_vlan,trunk_vlans,enabled
Gig1/0/1,User Access,access,20,,True
Po1,Uplink,trunk,,10;20;30,True
```
Si une donnée n'est pas nécessaire, laisser le champs totalement vide.

---

## ⚙️ Prérequis
- Python 3.7+
- pip

Installer les dépendances :
Dans le terminal , à la racine du projet : 
```bash
pip install -r requirements.txt
```
Sinon, installer les package importé dans le script mannuellement avec pip.

---

## ▶️ Exécution

```bash
python genconf.py
```

Le script va :
1. Lire les données renseignées depuis le répertoire `data/`
2. Charger et rendre les templates Jinja2 dans le répertoire `templates/`
3. Générer un fichier `.conf` pour chaque bloc de configuration dans le répertoire `output/<hostname>/`, ainsi qu'une configuration globale. Il génère un nouveau dossier portant le hostname du switch renseigné dans le fichier global_config.json.
⚠️ Si un dossier portant le même hostname que celui renseigné dans le JSON est déjà existant, il sera écrasé par la nouvelle généraiton du script.


---

## 🛠 Personnalisation
- Pour ajouter un nouveau bloc de config, créez un fichier Jinja2 dans `templates/` et ajoutez son nom dans la liste `template_list` dans `genconf.py`.
- Pour modifier la logique d’affichage d’une section (par exemple, SVI ou interfaces), modifiez les templates correspondants.

---

## 📊 Exemple de sortie
Fichier : `output/sw-core/sw-core_iface.conf`

```
interface Gig1/0/1
 description USER ACCESS
 switchport mode access
 switchport access vlan 20
 no shutdown
!
interface Port-channel1
 description UPLINK
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
 no shutdown
!
```

---

## 🚧 TODOs possibles
- Validation de schéma JSON
- Support du rendu dans plusieurs formats (YAML, CLI, etc.)
- ajout des templates routing
- Interface utilisateur simple (CLI interactive ou GUI)

---

## 📈 Auteur
Ryo

---

## 🌐 Licence
Ce projet est à usage interne / personnel. Peut être adapté librement pour les besoins de votre organisation.