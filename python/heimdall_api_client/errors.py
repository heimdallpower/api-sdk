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

