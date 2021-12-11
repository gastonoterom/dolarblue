"""Module for scraping exceptions"""
class ScrapingException(Exception):
    """Raised when scraping fails."""
    def __init__(self, msg):
        self.message = msg
        super().__init__(self.message)
