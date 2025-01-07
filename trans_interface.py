import os
import time
import requests
import yt_dlp
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog, messagebox

# Charger les variables d'environnement
load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLY_AI")
CURRENT_DIR = os.path.dirname(__file__)
TRANSCRIPTION_FOLDER = os.path.join(CURRENT_DIR, "transcriptions")
os.makedirs(TRANSCRIPTION_FOLDER, exist_ok=True)

# Téléchargement audio
def download_audio(youtube_url, output_dir="./"):
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        audio_file = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
    return audio_file

# Upload sur AssemblyAI
def upload_to_assemblyai(audio_file_path):
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    with open(audio_file_path, "rb") as f:
        response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, files={"file": f})
    response.raise_for_status()
    return response.json()["upload_url"]

# Demander transcription
def request_transcription(audio_url):
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    data = {"audio_url": audio_url, "language_code": "fr"}
    response = requests.post("https://api.assemblyai.com/v2/transcript", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["id"]

# Récupérer transcription
def get_transcription_result(transcription_id):
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    url = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        status = response.json()["status"]
        if status == "completed":
            return response.json()["text"]
        elif status == "failed":
            raise Exception("La transcription a échoué.")
        else:
            time.sleep(5)

# Sauvegarder transcription
def save_transcription_to_file(transcription_text, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(transcription_text)

# Processus complet
def process_youtube_video():
    youtube_url = url_entry.get()
    if not youtube_url:
        messagebox.showerror("Erreur", "Veuillez entrer un lien YouTube valide.")
        return

    try:
        # Téléchargement
        audio_path = download_audio(youtube_url)
        audio_url = upload_to_assemblyai(audio_path)
        transcription_id = request_transcription(audio_url)
        transcription_text = get_transcription_result(transcription_id)

        # Sauvegarde
        video_title = os.path.splitext(os.path.basename(audio_path))[0]
        output_file = os.path.join(TRANSCRIPTION_FOLDER, f"{video_title}.txt")
        save_transcription_to_file(transcription_text, output_file)

        messagebox.showinfo("Succès", f"Transcription terminée et sauvegardée dans :\n{output_file}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Interface utilisateur
root = tk.Tk()
root.title("Transcripteur YouTube")

tk.Label(root, text="Lien YouTube :").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

tk.Button(root, text="Transcrire", command=process_youtube_video).pack(pady=20)

root.mainloop()
