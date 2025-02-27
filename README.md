# Snapchat Story Downloader 2025

📱 Téléchargeur automatisé de stories Snapchat pour comptes publics (spécialisé pour les influenceurs français)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

Un script Python robuste pour télécharger automatiquement les stories Snapchat des comptes publics. Développé spécifiquement pour contourner les dernières protections de Snapchat (2025) et optimisé pour les comptes français.

## Fonctionnalités clés

- 🕒 Téléchargement automatique toutes les 24h
- 🖼️ Support simultané des photos (JPG) et vidéos (MP4)
- 📁 Organisation automatique des fichiers par date
- 🔒 Contournement des protections anti-bot de Snapchat
- 📊 Journalisation détaillée avec rotation des logs
- 🇫🇷 Localisation française intégrée
- 🛡️ Headers réalistes type appareil mobile Android

## Installation

1. Cloner le dépôt :

git clone https://github.com/votreutilisateur/snapchat-story-downloader.git
cd snapchat-story-downloader

## Utilisation

Commande de base :

python main.py [username]

Exemple :

python main.py bmsjoel

Paramètres optionnels :

- `--vpn fr` : Active le mode VPN (requiert configuration préalable)
- `--debug` : Active le mode debug détaillé

## Structure des fichiers

📂 downloads/
└── 📂 [username]_[date]
├── 📄 1_103045
mp4 ├── 📄 2_10
046.jpg └── 📄

## Configuration avancée

Modifier `config.json` pour :

{
"request_timeout":
30, "max_retr
es": 3, "use
_agents": [ "Mozilla/5.0 (Linux; Androi
14; SM-S901B)...", "Snapchat/15.84.0.0
A5
1DL; Android 14;
f

## Aspects légaux

⚠️ **Usage strictement éducatif**  
Ce script est fourni à titre de démonstration technique. Respectez :
- Les conditions d'utilisation de Snapchat
- Le droit d'auteur des créateurs
- La vie privée des utilisateurs

## Dépannage

Erreur courante | Solution
---------------|---------
`404 Not Found` | Vérifier que le compte existe et a des stories publiques
`Aucun contenu disponible` | Essayer avec un VPN localisé en France
`Téléchargement bloqué` | Mettre à jour les headers dans `config.json`

Activer les logs détaillés :

python main.py [username] --debug > debug.log 2>&1

## Contribution

Les contributions sont les bienvenues ! 
1. Forker le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commiter vos modifications (`git commit -m 'Add some amazing feature'`)
4. Pousser vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## Licence

Distribué sous licence MIT. Voir `LICENSE` pour plus d'informations.

---

**Auteur** : [KHERRAF Anis] 
**Contact** : [anis@kherraf.fr](mailto:anis@kherraf.fr)  
**Dernière mise à jour** : 27 février 2025
