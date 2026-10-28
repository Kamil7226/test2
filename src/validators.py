"""
src/validators.py
Funkcje bezpiecznego pobierania i walidacji danych wejściowych od użytkownika.
"""

def get_int_input(
        prompt: str,
        min_val: int = None,
        max_val: int = None,
    ) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Błąd: Pusta wartość. Spróbuj ponownie.")
            continue
        try:
            val = int(raw)
            if min_val is not None and val < min_val:
                print(f"Błąd: Wartość musi wynosić co najmniej {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Błąd: Wartość nie może przekraczać {max_val}.")
                continue
            return val
        except ValueError:
            print(f"Błąd: Wartość '{raw}' to nie jest poprawna liczba całkowita!")

def get_non_empty_string(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if not val:
            print("Błąd: Pole tekstowe nie może być puste.")
            continue
        return val

def get_float_input(
        prompt: str,
        min_val: float = None,
        max_val: float = None
        ) -> float:
    while True:
        raw = input(prompt).strip().replace(",", ".")
        if not raw:
            print("Błąd: Pusta wartość. Spróbuj ponownie.")
            continue
        try:
            val = float(raw)
            if min_val is not None and val < min_val:
                print(f"Błąd: Wartość musi wynosić co najmniej {min_val:.1f}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Błąd: Wartość nie może przekraczać {max_val:.1f}.")
                continue
            return val
        except ValueError:
            print(f"Błąd: '{raw}' to nie jest poprawna liczba!")