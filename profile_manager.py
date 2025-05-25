import json
import os

class ProfileManager:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load(self) -> dict:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Profile file not found: {self.filepath}")

        with open(self.filepath, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format in profile file: {e}")

    def save(self, profile_data: dict):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, ensure_ascii=False, indent=4)

    def exists(self) -> bool:
        return os.path.exists(self.filepath)
