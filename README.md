# ARCEP Chatbot

## Description
Ce projet est un chatbot développé en Flask pour répondre aux questions relatives à la réglementation.

## Structure du projet

arcep_chatbot/
│
├── arcep/                            # Environnement virtuel
│
├── docs/                             # Dossier pour stocker les documents réglementaires
│   ├── Règlementation_Rapports/
│   ├── Textes_Internationaux/
│   ├── Décrets/
│   ├── Lois/
│   ├── Arrêtés/
│   └── Décisions/
│       └── exemple_document.pdf      # Exemple de fichier PDF
│
├── data/                             # Fichier de questions/réponses
│   └── qa_pairs.xlsx                 # Fichier contenant les Q&A pour fine-tuning
│
├── static/                           # Fichiers CSS et JS
│   ├── css/
│   │   └── styles.css                # Fichier CSS pour le style du chatbot
│   └── js/
│       └── chatbot.js                # Fichier JS pour la logique du chatbot
│
├── templates/                        # Modèles HTML
│   ├── chatbot.html                  # Interface du chatbot
│   └── contact.html                  # Page Contactez-nous
│
├── tests/                             # Nouveau dossier pour les tests
│   ├── test_app.py                    # Tests pour app.py
│   └── test_fine_tune.py              # Tests pour fine_tune.py
│
├── app.py                            # Script principal de l'application Flask
├── fine_tune.py                      # Script pour fine-tuning et gestion des documents
├── requirements.txt                  # Dépendances du projet
└── README.md                         # Documentation du projet


## Installation
1. Créez un environnement virtuel et activez-le.
   ```bash
   python -m venv arcep
   source arcep/bin/activate  # Pour Linux/Mac
   .\arcep\Scripts\activate  # Pour Windows

2. pip install -r requirements.txt

3. python app.py

### Conclusion

Avec ces fichiers, vous avez une application Flask qui répond aux questions à partir d'un fichier Excel et de documents PDF. Vous pouvez également l'étendre avec des fonctionnalités supplémentaires selon vos besoins.

N'hésitez pas à poser d'autres questions ou à demander des précisions sur des parties spécifiques du code !
