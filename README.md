CineStream – Krok Milowy Tygodnia 5
======================================

To jest kompletna, zintegrowana wersja projektu. Wszystkie moduły znajdują się
w katalogu src.

STRUKTURA:
src/
  main.py          - uruchomienie aplikacji i menu
  models.py        - MediaTitle i Watchlist
  data.py          - dane początkowe
  storage.py       - zapis/odczyt JSON i eksport CSV
  services.py      - operacje na filmach
  validators.py    - walidacja danych
  test_models.py   - cztery wymagane autotesty

URUCHOMIENIE:
1. Otwórz folder CineStream_Tydzien_5 w PyCharm lub CLion.
2. Uruchom src/main.py albo w terminalu przejdź do katalogu src.
3. Wpisz: python main.py

TESTY:
W terminalu, będąc w katalogu src, wpisz:
python test_models.py

DANE:
Baza zapisuje się automatycznie w data/watchlist.json.
Eksport CSV trafia do exports/watchlist.csv.
Kopie zapasowe JSON są zapisywane w data/backups.

Uwaga:
To jest kompletna, działająca wersja projektu oparta na klasach OOP.
Dotychczasowy katalog filmów został przeniesiony do modelu MediaTitle.
