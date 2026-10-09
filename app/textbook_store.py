from pathlib import Path
import re
import shutil


class TextbookStore:

    def __init__(
        self,
        root_dir: str | Path = "data/textbooks",
    ):
        self.root_dir = Path(root_dir)

        self.root_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _make_book_id(
        self,
        filename: str,
    ) -> str:
        """
        Convert a PDF filename into a safe directory name.
        """

        name = Path(filename).stem.lower()

        name = re.sub(
            r"[^a-z0-9]+",
            "_",
            name,
        )

        name = name.strip("_")

        if not name:
            name = "textbook"

        return name

    def create_textbook(
        self,
        pdf_path: str | Path,
    ) -> tuple[str, Path]:

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        book_id = self._make_book_id(
            pdf_path.name
        )

        book_dir = (
            self.root_dir / book_id
        )

        book_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = (
            book_dir / "textbook.pdf"
        )

        shutil.copy2(
            pdf_path,
            destination,
        )

        return book_id, book_dir

    def get_textbook_dir(
        self,
        book_id: str,
    ) -> Path:

        book_dir = (
            self.root_dir / book_id
        )

        if not book_dir.exists():
            raise FileNotFoundError(
                f"Textbook not found: {book_id}"
            )

        return book_dir

    def list_textbooks(self) -> list[str]:

        return sorted(
            directory.name
            for directory in self.root_dir.iterdir()
            if directory.is_dir()
        )
        
    def create_textbook_from_bytes(
        self,
        filename: str,
        pdf_bytes: bytes,
    ) -> tuple[str, Path]:

        book_id = self._make_book_id(filename)

        book_dir = self.root_dir / book_id

        book_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = book_dir / "textbook.pdf"

        with open(destination, "wb") as file:
            file.write(pdf_bytes)

        return book_id, book_dir
