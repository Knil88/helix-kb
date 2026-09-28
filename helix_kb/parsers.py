"""Format-specific readers and folder scan."""

import csv
from io import StringIO
from pathlib import Path

from helix_kb.document import Document
from helix_kb.exceptions import (
    CorruptDocumentError,
    EmptyDocumentError,
    ParseError,
    UnsupportedFormatError,
)


class FormatParser:
    """Base parser. Subclasses must implement parse()."""

    def parse(self, path):
        """Read a file and return a Document."""
        raise NotImplementedError("Subclass must override parse()")


class TxtParser(FormatParser):
    """Parser for .txt files. Title = first non-empty line, else filename stem."""

    def parse(self, path):
        """Read a .txt file and return a Document."""
        p = Path(path)
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise CorruptDocumentError(path, f"encoding error: {exc}") from exc
        if not content.strip():
            raise EmptyDocumentError(path)
        for line in content.splitlines():
            if line.strip():
                title = line.strip()
                break
        else:
            title = p.stem
        return Document(title=title, content=content, source_path=str(p))


class MdParser(FormatParser):
    """Parser for .md files. Title = first # heading, else filename stem."""

    def parse(self, path):
        """Read a .md file and return a Document."""
        p = Path(path)
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise CorruptDocumentError(path, f"encoding error: {exc}") from exc
        if not content.strip():
            raise EmptyDocumentError(path)
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                title = stripped.lstrip("#").strip()
                break
        else:
            title = p.stem
        return Document(title=title, content=content, source_path=str(p))


class CsvParser(FormatParser):
    """Parser for .csv files. Title is the filename stem; content is one normalized row per record."""

    def parse(self, path):
        """Read a CSV file and return a Document with tabular text."""
        p = Path(path)
        try:
            raw = p.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise CorruptDocumentError(path, f"encoding error: {exc}") from exc
        if not raw.strip():
            raise EmptyDocumentError(path)
        reader = csv.DictReader(StringIO(raw))
        lines = []
        for row in reader:
            lines.append(" | ".join(f"{key}: {value}" for key, value in row.items()))
        normalized = "\n".join(lines)
        return Document(title=p.stem, content=normalized, source_path=str(p))


PARSERS = {
    ".txt": TxtParser(),
    ".md": MdParser(),
    ".csv": CsvParser(),
}


def parser_for(path):
    """Return the parser that matches the file suffix."""
    suffix = Path(path).suffix.lower()
    if suffix not in PARSERS:
        raise UnsupportedFormatError(path, suffix)
    return PARSERS[suffix]


def parse_folder(folder):
    """Parse every file in folder. Return (documents, errors). Never abort the scan."""
    documents = []
    errors = []
    for path in Path(folder).iterdir():
        if not path.is_file():
            continue
        try:
            parser = parser_for(path)
            documents.append(parser.parse(path))
        except ParseError as exc:
            errors.append({"path": str(path), "reason": str(exc)})
    return documents, errors
