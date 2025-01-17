#BU KODU ÇALIŞTIRMADAN ÖNCE readMe KISMINI DİKKATLİCE OKUYUNUZ

import os
import subprocess
import torch
from TTS.api import TTS
import pygame  # pygame ekleniyor
import librosa
import soundfile as sf
import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment  # pydub'ı ekledik
from moviepy.editor import VideoFileClip, AudioFileClip  # moviepy kullanarak video işleme
import tkinter as tk
from tkinter import filedialog, messagebox

# GPU/CPU seçim
device = "cuda" if torch.cuda.is_available() else "cpu"

# TTS modelini yükle
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Multilingual Speech Toolbox")
root.geometry("500x600")

# Global değişkenler
video = None
audio_file = None
final_audio_output = "final_audio_output.wav"

# Ses tanıma ve çeviri için dil listesi
languages = {
    "Türkçe": "tr",
    "İngilizce": "en",
    "İspanyolca": "es",
    "Fransızca": "fr",
    "Almanca": "de"
}

# Ses tanıma dili seçimi
default_recognition_language = tk.StringVar(value="Türkçe")
recognition_language_label = tk.Label(root, text="Ses Tanıma Dilini Seçin:")
recognition_language_label.pack(pady=5)

recognition_language_menu = tk.OptionMenu(root, default_recognition_language, *languages.keys())
recognition_language_menu.pack(pady=5)

# Çeviri hedef dili seçimi
default_translation_language = tk.StringVar(value="İngilizce")
translation_language_label = tk.Label(root, text="Çeviri Dilini Seçin:")
translation_language_label.pack(pady=5)

translation_language_menu = tk.OptionMenu(root, default_translation_language, *languages.keys())
translation_language_menu.pack(pady=5)

# Video dosyasını yükle ve ses çıkar
def load_video():
    global video, audio_file
    video_path = filedialog.askopenfilename(title="Video Dosyasını Seç", filetypes=(("MP4 Dosyaları", ".mp4"), ("Tüm Dosyalar", ".*")))
    if video_path:
        try:
            video = VideoFileClip(video_path)
            audio = video.audio
            audio_file = "extracted_audio.wav"
            audio.write_audiofile(audio_file, codec='pcm_s16le')
            messagebox.showinfo("Başarılı", "Ses dosyası başarıyla çıkarıldı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Ses çıkarma hatası: {str(e)}")

# Ses tanıma işlemi
def transcribe_audio():
    audio_wav = audio_file
    recognizer = sr.Recognizer()
    selected_language = default_recognition_language.get()  # Seçilen dil
    language_code = languages[selected_language] + "-" + languages[selected_language].upper()

    try:
        with sr.AudioFile(audio_wav) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=language_code)
            text_output.delete(1.0, tk.END)  # Önceki metni sil
            text_output.insert(tk.END, text)
            messagebox.showinfo("Başarılı", f"{selected_language} metni başarıyla alındı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Ses tanıma hatası: {str(e)}")

# Çeviri işlemi
def translate_text():
    text_to_translate = text_output.get(1.0, tk.END).strip()
    if text_to_translate:
        source_language = languages[default_recognition_language.get()]
        target_language = languages[default_translation_language.get()]
        translator = Translator()
        try:
            translated_text = translator.translate(text_to_translate, src=source_language, dest=target_language).text
            translated_output.delete(1.0, tk.END)  # Önceki çeviriyi sil
            translated_output.insert(tk.END, translated_text)
            messagebox.showinfo("Başarılı", f"Metin başarıyla çevrildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Çeviri hatası: {str(e)}")
    else:
        messagebox.showerror("Hata", "Lütfen önce bir metin girin.")

# Metni sese dönüştürme (Aksanlı ses taklit özelliğiyle)
def text_to_speech():
    text = translated_output.get(1.0, tk.END).strip()
    if text:
        try:
            # Örnekleme frekansını ve mono kanalı ayarla
            desired_sample_rate = 22050
            audio = AudioSegment.from_wav(audio_file)
            audio = audio.set_channels(1)
            audio = audio.set_frame_rate(desired_sample_rate)
            final_wav = "final_audio_mono_22050.wav"
            audio.export(final_wav, format="wav")

            # TTS ile aksanlı ses oluşturma
            target_language = languages[default_translation_language.get()]
            tts.tts_to_file(text=text, speaker_wav=final_wav, language=target_language, file_path=final_audio_output)
            messagebox.showinfo("Başarılı", "Metin başarıyla sese dönüştürüldü.")
        except Exception as e:
            messagebox.showerror("Hata", f"Ses dönüştürme hatası: {str(e)}")
    else:
        messagebox.showerror("Hata", "Lütfen önce çevrilmiş metin girin.")

# Pygame ile ses çalma
def play_audio():
    try:
        pygame.mixer.init(frequency=22050)
        pygame.mixer.music.load(final_audio_output)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        messagebox.showinfo("Başarılı", "Ses başarıyla çaldı.")
    except Exception as e:
        messagebox.showerror("Hata", f"Ses çalma hatası: {str(e)}")

# Videoyu ağız senkronizasyonu ile kaydet
def save_video_with_audio():
    try:
        if not os.path.exists("temp"):
            os.makedirs("temp")
        output_video_path = "senkronize_video/output.mp4"

        command = [
            "python", "Wav2Lip/inference.py",
            "--checkpoint_path", "Wav2Lip/checkpoints/wav2lip.pth",
            "--face", video.filename,
            "--audio", final_audio_output,
            "--outfile", output_video_path
        ]

        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        messagebox.showinfo("Başarılı", f"Ağız senkronizasyonu başarıyla tamamlandı: {output_video_path}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hata", f"Wav2Lip çalıştırılırken bir hata oluştu: {e.stderr}")
    except Exception as e:
        messagebox.showerror("Hata", f"Bilinmeyen bir hata oluştu: {str(e)}")

# GUI için butonları ve etiketleri oluştur
load_button = tk.Button(root, text="Video Yükle", command=load_video)
load_button.pack(pady=10)

transcribe_button = tk.Button(root, text="Ses Tanıma", command=transcribe_audio)
transcribe_button.pack(pady=10)

translate_button = tk.Button(root, text="Çevir", command=translate_text)
translate_button.pack(pady=10)

text_to_speech_button = tk.Button(root, text="Metni Sese Dönüştür", command=text_to_speech)
text_to_speech_button.pack(pady=10)

play_button = tk.Button(root, text="Sesi Çal", command=play_audio)
play_button.pack(pady=10)

save_video_button = tk.Button(root, text="Videoyu Kaydet (Ağız Senkronize)", command=save_video_with_audio)
save_video_button.pack(pady=10)

text_label = tk.Label(root, text="Tanınan Metin:")
text_label.pack(pady=5)
text_output = tk.Text(root, height=5, width=40)
text_output.pack(pady=5)

translated_label = tk.Label(root, text="Çevrilmiş Metin:")
translated_label.pack(pady=5)
translated_output = tk.Text(root, height=5, width=40)
translated_output.pack(pady=5)

root.mainloop()
