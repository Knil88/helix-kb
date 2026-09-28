"""Command-line interface for parsing a document folder."""

import argparse
import json
from pathlib import Path

from helix_kb.document import Document
from helix_kb.knowledge_base import KnowledgeBase
from helix_kb.parsers import parse_folder


def build_index(folder, index_path):
    """Parse folder, fill a KnowledgeBase, save JSON, return (kb, errors)."""
    documents, errors = parse_folder(folder)
    kb = KnowledgeBase()
    for doc in documents:
        kb.add(doc)
    Path(index_path).write_text(
        json.dumps([doc.to_dict() for doc in kb.list_all()], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return kb, errors


def load_index(index_path):
    """Rebuild a KnowledgeBase from a JSON index file."""
    payload = json.loads(Path(index_path).read_text(encoding="utf-8"))
    kb = KnowledgeBase()
    for row in payload:
        kb.add(
            Document(
                title=row["title"],
                content=row["content"],
                source_path=row["source_path"],
            )
        )
    return kb


def main(argv=None):
    """Parse a folder and print a short summary."""
    parser = argparse.ArgumentParser(
        description="Parse mixed-format documents into a knowledge-base index."
    )
    parser.add_argument(
        "--folder",
        default="archive",
        help="Folder of documents to parse (default: archive)",
    )
    parser.add_argument(
        "--index",
        default="kb_index.json",
        help="Path of the JSON index to write (default: kb_index.json)",
    )
    args = parser.parse_args(argv)

    folder = Path(args.folder)
    if not folder.is_dir():
        raise SystemExit(f"Folder not found: {folder}")

    kb, errors = build_index(folder, args.index)
    print(f"Processed: {len(kb.list_all())}")
    print(f"Skipped:   {len(errors)}")
    for item in errors:
        print(f"  - {item['path']} | {item['reason']}")
    print(f"Saved: {args.index}")
    print("Stats:", kb.stats())


if __name__ == "__main__":
    main()
