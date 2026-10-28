"""
src/storage.py
Warstwa persystencji danych: obsługa JSON, zapis atomowy, kopie zapasowe i CSV.
"""

import json
import csv
import os
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from src.data import DEFAULT_MOVIES


def get_data_dir() -> Path:
    """Zwraca ścieżkę do katalogu data/ i tworzy go, jeśli nie istnieje."""
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_exports_dir() -> Path:
    """Zwraca ścieżkę do katalogu exports/ na raporty CSV."""
    base_dir = Path(__file__).resolve().parent.parent
    exports_dir = base_dir / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    return exports_dir


def create_backup(source_file: Path, max_backups: int = 3) -> Path | None:
    """Tworzy rotowaną kopię zapasową (.bak) przed modyfikacją pliku bazy[cite: 30]."""
    if not source_file.exists():
        return None

    backup_dir = get_data_dir() / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{source_file.stem}_{stamp}.bak"

    shutil.copy2(source_file, backup_path)

    # Rotacja – utrzymujemy maksymalnie `max_backups` kopii
    existing_backups = sorted(backup_dir.glob(f"{source_file.stem}_*.bak"))
    while len(existing_backups) > max_backups:
        oldest = existing_backups.pop(0)
        oldest.unlink(missing_ok=True)

    return backup_path


def load_movies() -> list[dict]:
    """Bezpiecznie wczytuje bazę z pliku JSON z obsługą braków i uszkodzeń[cite: 6]."""
    file_path = get_data_dir() / "movies.json"

    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        atomic_save_movies(DEFAULT_MOVIES)
        return [dict(item) for item in DEFAULT_MOVIES]
    except json.JSONDecodeError:
        print(f"\n[OSTRZEŻENIE] Uszkodzony plik {file_path.name}! Załadowano domyślne dane awaryjne.")
        return [dict(item) for item in DEFAULT_MOVIES]


def atomic_save_movies(movies: list[dict]) -> None:
    """Zapisuje bazę w sposób całkowicie atomowy (tempfile + os.replace)[cite: 29]."""
    data_dir = get_data_dir()
    target_path = data_dir / "movies.json"

    if target_path.exists():
        create_backup(target_path, max_backups=3)

    with tempfile.NamedTemporaryFile(
            mode="w",
            dir=data_dir,
            prefix="movies_tmp_",
            suffix=".json",
            delete=False,
            encoding="utf-8"
    ) as tmp:
        json.dump(movies, tmp, indent=4, ensure_ascii=False)
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_name = tmp.name

    os.replace(temp_name, target_path)


def export_watchlist_to_csv(movies: list[dict]) -> int:
    """Eksportuje listę filmów do pliku CSV z nagłówkiem[cite: 9]."""
    file_path = get_exports_dir() / "watchlist.csv"
    fields = ["id", "title", "genre", "year", "rating", "platform"]

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(movies)

    return len(movies)