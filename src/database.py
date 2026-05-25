import json
import os
from typing import List, Dict, Any

class RepertoireDB:
    def __init__(self, file_path: str = "data/repertoire.json"):
        self.file_path = file_path
        self._ensure_storage_exists()

    NEXT_EVENT_FILE = "data/next_event.json"

    def _ensure_storage_exists(self):
        """Garante que a pasta data e o arquivo JSON existam ao iniciar."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def _ensure_file_exists(self, file_path: str, default_value: Any) -> None:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(default_value, f, ensure_ascii=False, indent=4)

    def load_songs(self) -> List[Dict[str, Any]]:
        """Carrega todas as músicas do arquivo JSON."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def load_next_event(self) -> str:
        """Carrega o texto do próximo evento."""
        self._ensure_file_exists(self.NEXT_EVENT_FILE, {"text": ""})
        try:
            with open(self.NEXT_EVENT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("text", "")
        except (json.JSONDecodeError, FileNotFoundError):
            return ""

    def save_next_event(self, text: str) -> None:
        """Grava o texto do próximo evento."""
        self._ensure_file_exists(self.NEXT_EVENT_FILE, {"text": ""})
        with open(self.NEXT_EVENT_FILE, 'w', encoding='utf-8') as f:
            json.dump({"text": text}, f, ensure_ascii=False, indent=4)

    def _save_all_songs(self, songs: List[Dict[str, Any]]):
        """Método interno para sobrescrever o arquivo JSON com a lista atualizada."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(songs, f, ensure_ascii=False, indent=4)

    def save_song(self, song_data: Dict[str, Any]):
        """Adiciona uma nova música ao repertório."""
        songs = self.load_songs()
        songs.append(song_data)
        self._save_all_songs(songs)

    def update_song(self, original_title: str, updated_data: Dict[str, Any]):
        """Busca uma música pelo título original e atualiza seus dados."""
        songs = self.load_songs()
        for idx, song in enumerate(songs):
            if song["title"].lower() == original_title.lower():
                songs[idx] = updated_data
                break
        self._save_all_songs(songs)

    def delete_song(self, title: str):
        """Remove uma música do acervo com base no título."""
        songs = self.load_songs()
        songs = [s for s in songs if s["title"].lower() != title.lower()]
        self._save_all_songs(songs)