import json
import os
from typing import List, Dict, Any

class RepertoireDB:
    def __init__(self, file_path: str = "data/repertoire.json"):
        self.file_path = file_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Garante que a pasta data e o arquivo JSON existam ao iniciar."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def load_songs(self) -> List[Dict[str, Any]]:
        """Carrega todas as músicas do arquivo JSON."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

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