import os
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Configuration de l'application Flask et de la base de données
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Modèle de base de données pour les patients
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    rendezvous = db.Column(db.String(100), nullable=False)
    presence = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Patient('{self.nom}', '{self.rendezvous}')"





# Route pour la page d'accueil
@app.route('/')
def index():
    patients = Patient.query.all()  # Récupérer tous les patients dans la base de données
    return render_template('index.html', patients=patients)


# Route pour ajouter un nouveau patient via l'enregistrement vocal
@app.route('/ajouter', methods=['POST'])
def ajouter_patient():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        rendezvous = request.form['rendezvous']


        # Sauvegarder le texte dans la base de données
        new_patient = Patient(nom=nom, rendezvous=rendezvous)
        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for('index'))


# Route pour marquer la présence du patient
@app.route('/presence/<int:id>', methods=['GET'])
def presence(id):
    patient = Patient.query.get_or_404(id)
    patient.presence = not patient.presence  # Inverser la présence
    db.session.commit()
    return redirect(url_for('index'))


# Initialisation de la base de données
with app.app_context():
    db.create_all()  # Créer la base de données si elle n'existe pas


if __name__ == '__main__':
    app.run(debug=True)
