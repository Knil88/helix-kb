"""In-memory knowledge base index."""

from pathlib import Path


class KnowledgeBase:
    """In-memory index of normalized documents."""

    def __init__(self):
        self.documents = []

    def add(self, doc):
        """Append a Document to the index."""
        self.documents.append(doc)

    def list_all(self):
        """Return all documents."""
        return list(self.documents)

    def search(self, query):
        """Return documents whose title or content contains query (case-insensitive)."""
        q = query.lower()
        results = []
        for doc in self.documents:
            if q in doc.title.lower() or q in doc.content.lower():
                results.append(doc)
        return results

    def filter_by_format(self, suffix):
        """Return documents whose source path has this suffix (e.g. '.md')."""
        s = suffix.lower()
        results = []
        for doc in self.documents:
            if Path(doc.source_path).suffix.lower() == s:
                results.append(doc)
        return results

    def stats(self):
        """Return totals, counts by format, and the three longest documents."""
        by_type = {}
        for doc in self.documents:
            ext = Path(doc.source_path).suffix.lower()
            by_type[ext] = by_type.get(ext, 0) + 1
        longest = sorted(
            self.documents,
            key=lambda doc: doc.word_count,
            reverse=True,
        )[:3]
        return {
            "total": len(self.documents),
            "by_type": by_type,
            "longest": [(doc.title, doc.word_count) for doc in longest],
        }
