# Nowa klasa abstrakcyjna do wyświetlania hitów
class Hit(ABC):

    @abstractmethod
    def show_hit(self, titles):
        pass


class MovieHit(Hit):

    def show_hit(self, titles):
        movies = [
            item for item in titles
            if isinstance(item, Movie)
            and item.rating is not None
        ]

        if movies:
            best = max(movies, key=lambda item: item.rating)
            print(f"Hit filmowy: {best.title} ({best.rating}/10)")
        else:
            print("Brak ocenionych filmów.")


class SeriesHit(Hit):

    def show_hit(self, titles):
        series = [
            item for item in titles
            if isinstance(item, Series)
            and item.rating is not None
        ]

        if series:
            best = max(series, key=lambda item: item.rating)
            print(f"Hit serialowy: {best.title} ({best.rating}/10)")
        else:
            print("Brak ocenionych seriali.")
