"""Normalized document model shared by every parser."""

import re
from pathlib import Path

DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})\b")


def extract_date(text):
    """Return the first date in text (YYYY-MM-DD or DD/MM/YYYY), or None."""
    match = DATE_RE.search(text)
    if match:
        return match.group(1)
    return None


class Document:
    """Normalized representation of a parsed document."""

    def __init__(self, title, content, source_path):
        """Store fields and compute word_count, excerpt, date and source_format."""
        self.title = title
        self.content = content
        self.source_path = str(source_path)
        self.source_format = Path(self.source_path).suffix.lower()
        self.word_count = len(content.split())
        self.excerpt = " ".join(content.split())[:80]
        self.date = extract_date(content)

    def to_dict(self):
        """Return a JSON-serializable dictionary of the document."""
        return {
            "title": self.title,
            "content": self.content,
            "source_path": self.source_path,
            "source_format": self.source_format,
            "word_count": self.word_count,
            "excerpt": self.excerpt,
            "date": self.date,
        }
