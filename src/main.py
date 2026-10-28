"""
src/main.py
Główny punkt wejścia do aplikacji CineStream
"""

from storage import load_movies, export_watchlist_to_csv
from validators import get_int_input
from services import display_movies, add_movie, filter_movies_by_genre


def print_menu() -> None:
    print("\n" + "=" * 40)
    print("      CINESTREAM - MENADŻER VOD      ")
    print("=" * 40)
    print("1. Wyświetl katalog filmów")
    print("2. Dodaj nowy film")
    print("3. Filtruj filmy po gatunku")
    print("4. Eksportuj katalog do CSV")
    print("5. Wyjście z programu")
    print("-" * 40)


def handle_menu_choice(choice: int, movies: list) -> bool:
    match choice:
        case 1:
            display_movies(movies)
        case 2:
            add_movie(movies)
        case 3:
            filter_movies_by_genre(movies)
        case 4:
            count = export_watchlist_to_csv(movies)
            print(f"\n[Sukces] Pomyślnie wyeksportowano {count} pozycji do pliku 'exports/watchlist.csv'!")
        case 5:
            print("\nZamykanie systemu CineStream. Do widzenia!")
            return False
        case _:
            print("\n[Błąd] Nieznana opcja. Wybierz wartość od 1 do 5.")
    return True


def main():
    # Wczytanie danych z trwałego pliku JSON na starcie aplikacji
    movies_catalog = load_movies()

    running = True
    while running:
        print_menu()
        user_choice = get_int_input("Wybierz opcję [1-5]: ", 1, 5)
        running = handle_menu_choice(user_choice, movies_catalog)


if __name__ == "__main__":
    main()