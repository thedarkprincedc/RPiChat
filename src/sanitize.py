import re
import unicodedata


def sanitize_filename(filename: str) -> str:
    """Return a filesystem-safe filename while preserving normal punctuation."""
    
    # Normalize Unicode characters.
    # Example: full-width "？" becomes normal "?"
    filename = unicodedata.normalize("NFKC", filename)

    # Remove control characters
    filename = re.sub(r"[\x00-\x1F\x7F]", "", filename)

    # Replace characters invalid on Windows
    # Apostrophe (') is intentionally preserved.
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Collapse multiple whitespace characters
    filename = re.sub(r"\s+", " ", filename).strip()

    # Windows doesn't allow filenames ending in a space or period
    filename = filename.rstrip(" .")

    # Avoid special path names
    if filename in (".", "..", ""):
        return "download"

    return filename