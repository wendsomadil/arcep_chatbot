import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
from fine_tune import find_answer  # Importer la fonction find_answer

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Route principale pour charger le chatbot
@app.route('/')
def chatbot():
    return render_template('chatbot.html')

# Route pour la page de contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route pour traiter la question de l'utilisateur
@app.route('/ask', methods=['POST'])
def ask():
    # Récupérer l'input utilisateur depuis la requête
    user_input = request.form.get('message', '').strip()
    print(f"Question posée par l'utilisateur : {user_input}")  # Pour débogage

    # Vérifier si l'entrée est vide
    if not user_input:
        return jsonify({'error': 'Veuillez entrer une question.'}), 400

    try:
        # Utiliser la fonction find_answer pour générer une réponse
        response = find_answer(user_input)
        print(f"Réponse obtenue : {response}")  # Pour débogage
        return jsonify({'response': response})  # Retourner la réponse au format JSON

    except Exception as e:
        print(f"Erreur : {e}")  # Afficher l'erreur dans la console pour le débogage
        return jsonify({'error': 'Une erreur est survenue lors de la recherche de la réponse.'}), 500

# Route pour le favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

# Route pour télécharger les documents (par exemple des PDFs)
@app.route('/docs/<path:filename>')
def download_file(filename):
    return send_from_directory('docs', filename)

# Gérer les erreurs 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Gérer les erreurs 500
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', error=str(e)), 500

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
