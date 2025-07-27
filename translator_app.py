

import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import threading
import io
import pygame

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Real-time Language Translator")
        self.root.geometry("700x700")
        self.root.configure(bg="#1e1e1e")

        self.recognizer = sr.Recognizer()
        self.translator = Translator()

        self.create_widgets()

    def create_widgets(self):
        font_label = ("Segoe UI", 11, "bold")
        font_text = ("Segoe UI", 11)
        pad = {"padx": 10, "pady": 5}

        # Speaker Language
        tk.Label(self.root, text="👤 Select Speaker's Language", font=font_label, bg="#1e1e1e", fg="white").pack(**pad)
        self.speaker_lang = tk.StringVar(self.root)
        self.speaker_lang.set("mr")
        tk.OptionMenu(self.root, self.speaker_lang, "hi", "bn", "te", "mr", "ta", "ur", "gu", "en", "zh-cn", "ru", "de", "fr", "ja", "ko", "pt").pack()

        # Listener Language
        tk.Label(self.root, text="🧏 Select Listener's Language", font=font_label, bg="#1e1e1e", fg="white").pack(**pad)
        self.listener_lang = tk.StringVar(self.root)
        self.listener_lang.set("en")
        tk.OptionMenu(self.root, self.listener_lang, "hi", "bn", "te", "mr", "ta", "ur", "gu", "en", "zh-cn", "ru", "de", "fr", "ja", "ko", "pt").pack()

        # Input Text
        tk.Label(self.root, text="🎙️ Input Text", font=font_label, bg="#1e1e1e", fg="white").pack(**pad)
        self.input_text = tk.Text(self.root, height=6, font=font_text, bg="#2b2b2b", fg="white", insertbackground="white")
        self.input_text.pack(padx=20, pady=5, fill="both")

        # Buttons
        self.create_button("🎧 Recognize and Speak", self.recognize_and_speak, "#6a5acd")
        self.create_button("🌐 Translate", self.translate_text, "#1e90ff")
        self.create_button("🔊 Speak Translation", self.speak_translation, "#32cd32")

        # Output Text
        tk.Label(self.root, text="📝 Translated Text", font=font_label, bg="#1e1e1e", fg="white").pack(**pad)
        self.output_text = tk.Text(self.root, height=6, font=font_text, bg="#2b2b2b", fg="white", insertbackground="white")
        self.output_text.pack(padx=20, pady=5, fill="both")

    def create_button(self, text, command, color):
        btn = tk.Button(self.root, text=text, command=command, bg=color, fg="white", font=("Segoe UI", 11, "bold"), relief="flat", padx=10, pady=6)
        btn.pack(pady=5)
        btn.bind("<Enter>", lambda e: btn.config(bg="gray"))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))

    def recognize_and_speak(self):
        lang = self.speaker_lang.get()
        threading.Thread(target=self.recognize_and_speak_thread, args=(lang,)).start()

    def recognize_and_speak_thread(self, lang):
        with sr.Microphone() as source:
            print("🎤 Listening...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio, language=lang)
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, text)
                self.speak_text(text, lang)
            except sr.UnknownValueError:
                messagebox.showerror("Recognition Error", "Could not understand the audio")
            except sr.RequestError:
                messagebox.showerror("Recognition Error", "Google API unavailable")
            except Exception as e:
                messagebox.showerror("Recognition Error", str(e))

    def translate_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if text:
            try:
                translated = self.translator.translate(text, src=self.speaker_lang.get(), dest=self.listener_lang.get()).text
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, translated)
            except Exception as e:
                messagebox.showerror("Translation Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Enter some text to translate")

    def speak_translation(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if text:
            self.speak_text(text, self.listener_lang.get())
        else:
            messagebox.showwarning("TTS Error", "Nothing to speak")

    def speak_text(self, text, lang):
        try:
            tts = gTTS(text=text, lang=lang)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(fp, 'mp3')  # Needs pygame 2.0.1+
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
        except Exception as e:
            messagebox.showerror("TTS Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()

