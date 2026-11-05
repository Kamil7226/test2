"""
src/services.py
Wyświetlanie, dodawanie oraz filtrowanie filmów.
"""

from validators import get_non_empty_string, get_int_input, get_float_input
from storage import atomic_save_movies, make_watchlist
from models import MediaTitle


def display_movies(movies: list[dict]) -> None:
    if not movies:
        print("\n[Informacja] Brak filmów w bazie CineStream\n")
        return

    header = f"| {'ID':<3} | {'Tytuł filmu':<30} | {'Gatunek':<12} | {'Rok':<4} | {'Ocena':<5} | {'Platforma':<12} |"
    sep = "-" * len(header)

    print(f"\n{sep}\n{header}\n{sep}")

    for m in movies:
        print(
            f"| {m['id']:<3} "
            f"| {m['title']:<30} "
            f"| {m['genre']:<12} "
            f"| {m['year']:<4} "
            f"| {m['rating'] if m['rating'] is not None else '-':<5} "
            f"| {m['platform']:<12} |"
        )

    print(f"{sep}\nŁącznie pozycji: {len(movies)}\n")


def add_movie(movies: list) -> None:
    print("\n--- DODAWANIE NOWEGO FILMU DO CINESTREAM ---")

    new_id = max((m["id"] for m in movies), default=0) + 1

    title = get_non_empty_string("Podaj tytuł filmu: ")
    genre = get_non_empty_string("Podaj gatunek (np. Sci-Fi, Dramat): ")
    year = get_int_input("Podaj rok premiery (1900-2030): ", min_val=1900, max_val=2030)
    is_watched = get_int_input("Czy obejrzany? (1 = tak, 0 = nie): ", 0, 1) == 1
    rating = get_float_input("Podaj ocenę (1.0 - 10.0): ", 1.0, 10.0) if is_watched else None
    duration_min = get_int_input("Podaj czas trwania w minutach: ", 1)
    platform = get_non_empty_string("Podaj platformę VOD (np. Netflix, HBO Max): ")

    # Walidacja domenowa odbywa się w modelu, a nie tylko w CLI.
    MediaTitle(new_id, title, year, rating, genre, is_watched, duration_min)

    new_movie = {
        "id": new_id,
        "title": title,
        "genre": genre,
        "year": year,
        "rating": rating,
        "platform": platform,
        "is_watched": is_watched,
        "duration_min": duration_min
    }

    movies.append(new_movie)

    # Automatyczny, bezpieczny zapis atomowy na dysku wraz z kopią .bak
    atomic_save_movies(movies)

    print(f"\n[Sukces] Film '{title}' został pomyślnie dodany do katalogu i zapisany (ID: {new_id})!")


def filter_movies_by_genre(movies: list) -> None:
    """Proste filtrowanie filmów po gatunku."""
    if not movies:
        print("\n[Brak filmów do przefiltrowania]")
        return

    search_genre = get_non_empty_string("Podaj gatunek do wyszukania: ").lower()
    filtered = [m for m in movies if search_genre in m["genre"].lower()]

    if not filtered:
        print(f"\n[Informacja] Nie znaleziono filmów dla gatunku: '{search_genre}'")
    else:
        print(f"\n--- Wyniki filtrowania dla gatunku: '{search_genre}' ---")
        display_movies(filtered)

def show_total_runtime(movies: list[dict]) -> None:
    watchlist = make_watchlist(movies)
    print(f"\nŁączny czas trwania filmów: {watchlist.total_runtime_hours():.2f} godz.\n")
