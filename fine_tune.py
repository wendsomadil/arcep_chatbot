import os
import logging
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Utilisation du modèle français
model_name = "CATIE-AQ/QAmembert-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Création du pipeline pour question-answering
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

# Fonction pour vérifier si un PDF est valide
def is_valid_pdf(file_path):
    try:
        pdf = fitz.open(file_path)
        if pdf.page_count > 0:
            return True
    except Exception:
        return False
    return False

# Fonction pour extraire le texte d'un PDF avec fallback OCR
def extract_text_from_pdf(file_path):
    text = ""
    try:
        pdf = fitz.open(file_path)
        for page_num in range(pdf.page_count):
            page_text = pdf[page_num].get_text("text")
            if page_text.strip():
                text += page_text + "\n"
            else:
                logging.warning(f"Page {page_num + 1} vide dans {file_path}, tentative d'OCR.")
                text += extract_text_from_pdf_with_ocr(file_path)
    except Exception as e:
        logging.error(f"Erreur lors de l'extraction du texte du PDF {file_path}: {e}")
        text = extract_text_from_pdf_with_ocr(file_path)
    return text

# Extraction de texte via OCR en cas d'échec de l'extraction directe
def extract_text_from_pdf_with_ocr(file_path):
    text = ""
    try:
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img, lang='fra') + "\n"  # Utiliser 'fra' pour le français
    except Exception as e:
        logging.error(f"Erreur lors de l'OCR sur {file_path}: {e}")
    return text

# Fonction pour charger tous les documents PDF d'un dossier (et sous-dossiers)
def load_documents_from_folder(folder_path):
    document_texts = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                full_path = os.path.join(root, file)
                if is_valid_pdf(full_path):
                    logging.info(f"Extraction du fichier PDF valide : {full_path}")
                    document_texts[full_path] = extract_text_from_pdf(full_path)
                else:
                    logging.warning(f"Le fichier PDF {full_path} est corrompu, tentative d'OCR.")
                    document_texts[full_path] = extract_text_from_pdf_with_ocr(full_path)
    return document_texts

# Charger tous les documents PDF dans le dossier 'docs' et ses sous-dossiers
docs_texts = load_documents_from_folder('docs')

# Fonction principale pour trouver une réponse à une question dans les documents
def find_answer(question):
    logging.info(f"Recherche de la réponse pour la question: {question}")
    best_answer = None
    best_score = None

    try:
        for doc_path, doc_text in docs_texts.items():
            # Utilisation du modèle pour répondre à partir du texte du document
            inputs = {
                "question": question,
                "context": doc_text
            }
            result = qa_pipeline(inputs)
            if result and "answer" in result:
                answer = result["answer"]
                score = result["score"]
                logging.info(f"Réponse trouvée dans {doc_path} avec score {score}: {answer}")
                # Garder la réponse avec le score le plus élevé
                if best_score is None or score > best_score:
                    best_score = score
                    best_answer = f"Réponse trouvée dans le document '{os.path.basename(doc_path)}': {answer}"
        if best_answer:
            return best_answer
        else:
            return "Désolé, je n'ai pas trouvé de réponse pertinente."
    except Exception as e:
        logging.error(f"Erreur lors de la recherche de la réponse : {e}")
        return "Une erreur est survenue lors du traitement de la question."
