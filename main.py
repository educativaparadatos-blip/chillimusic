main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
import yt_dlp
import os

MUSIC_DIR = '/sdcard/Music/ChilliMusic'

class ChilliMusicApp(App):
    def build(self):
        self.title = 'Chilli Music'
        self.sound = None
        os.makedirs(MUSIC_DIR, exist_ok=True)
        root = BoxLayout(orientation='vertical', padding=15, spacing=10)
        title = Label(text='Chilli Music', font_size=28, bold=True, color=(1, 0.3, 0.1, 1), size_hint_y=None, height=50)
        root.add_widget(title)
        self.url_input = TextInput(hint_text='Pega cualquier link (YouTube, TikTok, FB...)', size_hint_y=None, height=50)
        root.add_widget(self.url_input)
        btn_download = Button(text='Descargar Audio', size_hint_y=None, height=50, background_color=(1, 0.3, 0.1, 1))
        btn_download.bind(on_press=self.download_audio)
        root.add_widget(btn_download)
        self.status = Label(text='Listo para descargar', size_hint_y=None, height=35, color=(0.8, 0.8, 0.8, 1))
        root.add_widget(self.status)
        scroll = ScrollView()
        self.songs_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.songs_layout.bind(minimum_height=self.songs_layout.setter('height'))
        scroll.add_widget(self.songs_layout)
        root.add_widget(scroll)
        btn_refresh = Button(text='Actualizar Lista', size_hint_y=None, height=45, background_color=(0.2, 0.2, 0.2, 1))
        btn_refresh.bind(on_press=self.load_songs)
        root.add_widget(btn_refresh)
        self.load_songs()
        return root

    def download_audio(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status.text = 'Ingresa un link primero'
            return
        self.status.text = 'Descargando...'
        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': f'{MUSIC_DIR}/%(title)s.%(ext)s'}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status.text = 'Descarga completada'
            self.url_input.text = ''
            self.load_songs()
        except Exception as e:
            self.status.text = f'Error: {str(e)[:40]}'

    def load_songs(self, instance=None):
        self.songs_layout.clear_widgets()
        if not os.path.exists(MUSIC_DIR):
            return
        files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3','.m4a','.webm','.ogg'))]
        if not files:
            self.songs_layout.add_widget(Label(text='No hay canciones aun', color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=40))
            return
        for f in files:
            btn = Button(text=f[:35], size_hint_y=None, height=45, background_color=(0.15, 0.15, 0.15, 1))
            btn.bind(on_press=lambda x, name=f: self.play_song(name))
            self.songs_layout.add_widget(btn)

    def play_song(self, filename):
        if self.sound:
            self.sound.stop()
        path = os.path.join(MUSIC_DIR, filename)
        self.sound = SoundLoader.load(path)
        if self.sound:
            self.sound.play()
            self.status.text = f'Reproduciendo: {filename[:30]}'
        else:
            self.status.text = 'No se pudo reproducir'

if __name__ == '__main__':
    ChilliMusicApp().run()
  
