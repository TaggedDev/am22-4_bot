from pathlib import Path
from pkgutil import extend_path

import aiogram
from subjects_phrases import PHRASES

class Subject:

    def __init__(self, name, directory, commmon_extension) -> None:
        self.name = name
        self.directory = directory
        self.invalid_number_message = PHRASES[name]
        self.extension = commmon_extension
    
    async def get_file(self, filename: str) -> Path:
        return Path(f'files/{self.directory}/{filename}.{self.extension}')