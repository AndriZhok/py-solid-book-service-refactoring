import json
import xml.etree.ElementTree as TALON
from abc import ABC, abstractmethod
from typing import List, Tuple, Union


# --- Abstractions ---


class DisplayStrategy(ABC):
    @abstractmethod
    def display(self, content: str) -> None:
        pass


class PrintStrategy(ABC):
    @abstractmethod
    def print(self, title: str, content: str) -> None:
        pass


class SerializeStrategy(ABC):
    @abstractmethod
    def serialize(self, title: str, content: str) -> str:
        pass


# --- Implementations ---


class ConsoleDisplay(DisplayStrategy):
    def display(self, content: str) -> None:
        print(content)


class ReverseDisplay(DisplayStrategy):
    def display(self, content: str) -> None:
        print(content[::-1])


class ConsolePrint(PrintStrategy):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book: {title}...")
        print(content)


class ReversePrint(PrintStrategy):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])


class JsonSerialize(SerializeStrategy):
    def serialize(self, title: str, content: str) -> str:
        return json.dumps({"title": title, "content": content})


class XmlSerialize(SerializeStrategy):
    def serialize(self, title: str, content: str) -> str:
        root = TALON.Element("book")
        title_el = TALON.SubElement(root, "title")
        title_el.text = title
        content_el = TALON.SubElement(root, "content")
        content_el.text = content
        return TALON.tostring(root, encoding="unicode")


# --- Book Entity ---


class Book(object):
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content


# --- Main Controller ---


class BookController(object):
    def __init__(self, book: Book):
        self.book = book

    def display(self, strategy: DisplayStrategy) -> None:
        strategy.display(self.book.content)

    def print_book(self, strategy: PrintStrategy) -> None:
        strategy.print(self.book.title, self.book.content)

    def serialize(self, strategy: SerializeStrategy) -> str:
        return strategy.serialize(self.book.title, self.book.content)


# --- Main Logic ---


def main(book: Book, commands: List[Tuple[str, str]]) -> Union[None, str]:
    controller = BookController(book)

    strategy_map = {
        "display": {"console": ConsoleDisplay(), "reverse": ReverseDisplay()},
        "print": {"console": ConsolePrint(), "reverse": ReversePrint()},
        "serialize": {"json": JsonSerialize(), "xml": XmlSerialize()},
    }

    for cmd, method_type in commands:
        strategy = strategy_map.get(cmd, {}).get(method_type)
        if not strategy:
            raise ValueError(f"Unknown combination: {cmd} {method_type}")

        if cmd == "display":
            controller.display(strategy)
        elif cmd == "print":
            controller.print_book(strategy)
        elif cmd == "serialize":
            return controller.serialize(strategy)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
