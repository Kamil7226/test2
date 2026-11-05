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
from data import MOVIES_CATALOG
from models import MediaTitle, Watchlist


def get_data_dir() -> Path:
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_exports_dir() -> Path:
    base_dir = Path(__file__).resolve().parent.parent
    exports_dir = base_dir / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    return exports_dir


def create_backup(source_file: Path, max_backups: int = 3) -> Path | None:
    if not source_file.exists():
        return None

    backup_dir = get_data_dir() / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%m%d_%H%M%S")
    backup_path = backup_dir / f"{source_file.stem}_{stamp}.bak"

    shutil.copy2(source_file, backup_path)

    existing_backups = sorted(backup_dir.glob(f"{source_file.stem}_*.bak"))
    while len(existing_backups) > max_backups:
        oldest = existing_backups.pop(0)
        oldest.unlink(missing_ok=True)

    return backup_path


def movie_to_model(movie: dict) -> MediaTitle:
    """Konwersja starego rekordu; starsze filmy z oceną uznajemy za obejrzane."""
    return MediaTitle(
        title_id=movie.get("title_id", movie.get("id")),
        title=movie["title"], year=movie["year"], rating=movie.get("rating"),
        genre=movie["genre"],
        is_watched=movie.get("is_watched", movie.get("rating") is not None),
        duration_min=movie.get("duration_min", 120),
    )


def model_to_movie(model: MediaTitle, platform: str = "") -> dict:
    return {"id": model.title_id, "title": model.title, "genre": model.genre,
            "year": model.year, "rating": model.rating, "platform": platform,
            "is_watched": model.is_watched, "duration_min": model.duration_min}


def make_watchlist(movies: list[dict]) -> Watchlist:
    return Watchlist(titles=[movie_to_model(movie) for movie in movies])


def load_movies() -> list[dict]:
    """Bezpiecznie wczytuje bazę z pliku JSON z obsługą braków i uszkodzeń."""
    file_path = get_data_dir() / "movies.json"

    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            payload = json.load(f)
            if isinstance(payload, list):
                return [model_to_movie(movie_to_model(m), m.get("platform", "")) for m in payload]
            watchlist = Watchlist.from_dict(payload)
            platforms = payload.get("platforms", {})
            return [model_to_movie(title, platforms.get(str(title.title_id), ""))
                    for title in watchlist.titles]
    except FileNotFoundError:
        atomic_save_movies(MOVIES_CATALOG)
        return [dict(item) for item in MOVIES_CATALOG]
    except json.JSONDecodeError:
        print(f"\n[OSTRZEŻENIE] Uszkodzony plik {file_path.name}! Załadowano domyślne dane awaryjne.")
        return [dict(item) for item in MOVIES_CATALOG]


def atomic_save_movies(movies: list[dict]) -> None:
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
        payload = make_watchlist(movies).to_dict()
        payload["platforms"] = {str(m["id"]): m.get("platform", "") for m in movies}
        json.dump(payload, tmp, indent=4, ensure_ascii=False)
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_name = tmp.name

    os.replace(temp_name, target_path)


def export_watchlist_to_csv(movies: list[dict]) -> int:
    """Eksportuje listę filmów do pliku CSV z nagłówkiem"""
    file_path = get_exports_dir() / "watchlist.csv"
    fields = ["id", "title", "genre", "year", "rating", "platform", "is_watched", "duration_min"]

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(movies)

    return len(movies)