"""Custom exceptions for document parsing."""


class ParseError(Exception):
    """Base error for document parsing."""


class UnsupportedFormatError(ParseError):
    """Raised when the file suffix has no parser."""

    def __init__(self, path, suffix):
        super().__init__(f"Unsupported format '{suffix}' for {path}")
        self.path = path
        self.suffix = suffix


class EmptyDocumentError(ParseError):
    """Raised when the document has no usable text."""

    def __init__(self, path):
        super().__init__(f"Empty document: {path}")
        self.path = path


class CorruptDocumentError(ParseError):
    """Raised when the document cannot be decoded or is malformed."""

    def __init__(self, path, reason):
        super().__init__(f"Corrupt document {path}: {reason}")
        self.path = path
        self.reason = reason
