class HeimdallApiError(Exception):
    """
    Raised when the Heimdall API returns a non-successful HTTP response.
    """

    def __init__(self, message: str, status_code: int, request_url: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.request_url = request_url

    def is_transient(self) -> bool:
        """Returns True if the error is likely transient and safe to retry."""
        return self.status_code in {502, 503, 504}


def body_preview(content: bytes, max_chars: int = 200) -> str:
    """Returns a UTF-8 decoded, whitespace-collapsed preview of a response body."""
    text = content.decode("utf-8", errors="replace").strip()
    # Collapse runs of whitespace/newlines (common in HTML error pages)
    import re

    text = re.sub(r"\s+", " ", text)
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text or "(empty body)"
