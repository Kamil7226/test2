"""Autotesty wymagane w laboratorium 3.1. Uruchom: python test_models.py"""
from models import MediaTitle, Watchlist


def test_instantiation():
    movie = MediaTitle(1, 'Incepcja', 2010, 8.8, 'Sci-Fi', True, 148)
    watchlist = Watchlist(1, [movie])
    assert watchlist.titles == [movie]
    assert watchlist.total_runtime_hours() == round(148 / 60, 2)
    assert 'Incepcja' in str(movie)


def test_invariants():
    try:
        MediaTitle(2, 'Nieobejrzany', 2020, 8.0, 'Dramat', False, 90)
        assert False, 'Oceniono nieobejrzany film'
    except ValueError:
        pass
    movie = MediaTitle(3, 'Film', 2020, None, 'Dramat', False, 90)
    try:
        movie.rating = 5.0
        assert False, 'Setter zaakceptował ocenę'
    except ValueError:
        pass
    movie.is_watched = True
    movie.rating = 9.0
    assert movie.rating == 9.0
    try:
        Watchlist(titles=[movie, movie])
        assert False, 'Zduplikowano ID'
    except ValueError:
        pass


def test_sorting():
    movies = [MediaTitle(1, 'A', 2000, 6.0, 'Dramat', True, 90),
              MediaTitle(2, 'B', 2000, 9.0, 'Dramat', True, 90),
              MediaTitle(3, 'C', 2000, None, 'Dramat', False, 90)]
    movies.sort()
    assert [m.title_id for m in movies] == [2, 1, 3]


def test_roundtrip():
    original = Watchlist(7, [MediaTitle(1, 'A', 2000, 7.0, 'Dramat', True, 100),
                             MediaTitle(2, 'B', 2020, None, 'Sci-Fi', False, 110)])
    restored = Watchlist.from_dict(original.to_dict())
    assert original == restored
    assert original is not restored


if __name__ == '__main__':
    for test in (test_instantiation, test_invariants, test_sorting, test_roundtrip):
        test()
        print(f'[OK] {test.__name__}')
    print('Wszystkie 4 testy zaliczone.')
