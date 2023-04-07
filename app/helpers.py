import string
import random
from urllib.parse import urlparse
from app.constants import MAX_URL_DISPLAY_LENGTH

def create_short_link():
    """Generate random alphanumeric short code"""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    code = "".join([random.choice(chars) for _ in range(8)])
    return code

def validate_url(url):
    """Validate URL being shortened, only allow http and https protocols"""
    try:
        result = urlparse(url)
        valid_scheme = result.scheme in {"http", "https"}
        return valid_scheme and result.netloc
    except ValueError:
        return False

def truncate_url(url):
    """Truncate long URLs for display"""
    if len(url) <= MAX_URL_DISPLAY_LENGTH:
        return url
    return url[:MAX_URL_DISPLAY_LENGTH] + "..."
