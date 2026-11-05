"""Modele obiektowe CineStream – laboratorium 3.1."""
from __future__ import annotations
from typing import Any
from math import isfinite


class MediaTitle:
    def __init__(self, title_id: int, title: str, year: int, rating: float | None,
                 genre: str, is_watched: bool, duration_min: int) -> None:
        if type(title_id) is not int or title_id <= 0:
            raise ValueError('ID musi być dodatnią liczbą całkowitą.')
        if not isinstance(title, str) or not title.strip():
            raise ValueError('Tytuł nie może być pusty.')
        if type(year) is not int or not 1900 <= year <= 2030:
            raise ValueError('Nieprawidłowy rok premiery.')
        if not isinstance(genre, str) or not genre.strip():
            raise ValueError('Gatunek nie może być pusty.')
        if type(is_watched) is not bool:
            raise TypeError('is_watched musi być wartością bool.')
        if type(duration_min) is not int or duration_min <= 0:
            raise ValueError('Czas trwania musi być dodatni.')
        self._title_id = title_id
        self.title = title.strip()
        self.year = year
        self.genre = genre.strip()
        self.duration_min = duration_min
        self._is_watched = is_watched
        self._rating: float | None = None
        self.rating = rating

    @property
    def title_id(self) -> int:
        return self._title_id

    @property
    def is_watched(self) -> bool:
        return self._is_watched

    @is_watched.setter
    def is_watched(self, value: bool) -> None:
        if type(value) is not bool:
            raise TypeError('is_watched musi być wartością bool.')
        if not value and self.rating is not None:
            raise ValueError('Usuń ocenę przed oznaczeniem filmu jako nieobejrzany.')
        self._is_watched = value

    @property
    def rating(self) -> float | None:
        return self._rating

    @rating.setter
    def rating(self, value: float | None) -> None:
        if value is None:
            self._rating = None
            return
        if not self.is_watched:
            raise ValueError('Nie można ocenić nieobejrzanego filmu.')
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError('Ocena musi być liczbą.')
        if not isfinite(value) or not 1.0 <= value <= 10.0:
            raise ValueError('Ocena musi być w zakresie 1.0–10.0.')
        self._rating = round(float(value), 1)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MediaTitle) and self.title_id == other.title_id

    def __lt__(self, other: MediaTitle) -> bool:
        if not isinstance(other, MediaTitle):
            return NotImplemented
        return (-(self.rating or 0), self.title.casefold()) < (-(other.rating or 0), other.title.casefold())

    def __repr__(self) -> str:
        return (f'MediaTitle(title_id={self.title_id!r}, title={self.title!r}, '
                f'year={self.year!r}, rating={self.rating!r}, genre={self.genre!r}, '
                f'is_watched={self.is_watched!r}, duration_min={self.duration_min!r})')

    def __str__(self) -> str:
        return f'[{self.title_id}] {self.title} ({self.year}) – {self.rating if self.rating is not None else "bez oceny"}'

    def to_dict(self) -> dict[str, Any]:
        return {'title_id': self.title_id, 'title': self.title, 'year': self.year,
                'rating': self.rating, 'genre': self.genre, 'is_watched': self.is_watched,
                'duration_min': self.duration_min}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MediaTitle:
        return cls(**data)


class Watchlist:
    def __init__(self, watchlist_id: int = 1, titles: list[MediaTitle] | None = None) -> None:
        self.watchlist_id = watchlist_id
        self._titles: list[MediaTitle] = []
        for title in titles or []:
            self.add_title(title)

    @property
    def titles(self) -> list[MediaTitle]:
        return list(self._titles)

    def add_title(self, title: MediaTitle) -> None:
        if not isinstance(title, MediaTitle):
            raise TypeError('Można dodawać tylko obiekty MediaTitle.')
        if title in self._titles:
            raise ValueError('Film o takim ID już istnieje.')
        self._titles.append(title)

    def total_runtime_hours(self) -> float:
        return round(sum(title.duration_min for title in self._titles) / 60, 2)

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Watchlist) and self.watchlist_id == other.watchlist_id
                and [t.to_dict() for t in self._titles] == [t.to_dict() for t in other._titles])

    def __repr__(self) -> str:
        return f'Watchlist(watchlist_id={self.watchlist_id!r}, titles={self._titles!r})'

    def __str__(self) -> str:
        return f'Watchlist #{self.watchlist_id}: {len(self._titles)} filmów, {self.total_runtime_hours()} h'

    def to_dict(self) -> dict[str, Any]:
        return {'watchlist_id': self.watchlist_id, 'titles': [title.to_dict() for title in self._titles]}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Watchlist:
        return cls(data['watchlist_id'], [MediaTitle.from_dict(item) for item in data['titles']])
