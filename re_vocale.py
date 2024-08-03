import streamlit as st
import speech_recognition as sr
import threading
import time

# Initialisation de la reconnaissance vocale
recognizer = sr.Recognizer()
microphone = sr.Microphone()
transcribed_text = ""
is_paused = False
api_choice = "Google"
language = "fr-FR"

# Fonction de transcription de la parole
def transcribe_speech():
    global transcribed_text, is_paused, api_choice, language
    with microphone as source:
        while not is_paused:
            try:
                audio = recognizer.listen(source, timeout=5)
                if api_choice == "Google":
                    text = recognizer.recognize_google(audio, language=language)
                elif api_choice == "Sphinx":
                    text = recognizer.recognize_sphinx(audio)
                # Ajoutez d'autres API ici...
                else:
                    st.error(f"API {api_choice} non supportée.")
                    return

                transcribed_text += text + " "
                st.session_state.transcribed_text = transcribed_text
                st.text_area("Texte Transcrit", value=transcribed_text, height=200)
            except sr.RequestError as e:
                st.error(f"Erreur de connexion avec l'API: {str(e)}")
            except sr.UnknownValueError:
                st.warning("Impossible de comprendre l'audio.")
            except Exception as e:
                st.error(f"Erreur inattendue: {str(e)}")
            time.sleep(1)

# Interface utilisateur avec Streamlit
st.title("Application de Reconnaissance Vocale")

api_options = ["Google", "Sphinx", "IBM", "Wit", "Bing", "Houndify", "Azure"]
api_choice = st.selectbox("Sélectionnez l'API de Reconnaissance Vocale:", api_options)

lang_options = {"Français": "fr-FR", "Anglais": "en-US", "Espagnol": "es-ES"}
language = st.selectbox("Sélectionnez la Langue:", list(lang_options.keys()))
language = lang_options[language]

if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

# Boutons de contrôle
start_button = st.button("Démarrer")
pause_button = st.button("Pause")
resume_button = st.button("Reprendre")
save_button = st.button("Enregistrer Texte")

# Actions des boutons
if start_button:
    is_paused = False
    threading.Thread(target=transcribe_speech).start()

if pause_button:
    is_paused = True

if resume_button:
    is_paused = False
    threading.Thread(target=transcribe_speech).start()

if save_button:
    with open("transcription.txt", "w") as file:
        file.write(st.session_state.transcribed_text)
    st.success("Texte transcrit enregistré avec succès!")

# Affichage du texte transcrit
st.text_area("Texte Transcrit", value=st.session_state.transcribed_text, height=200)
