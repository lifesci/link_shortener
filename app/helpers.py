import string
import random
from urllib.parse import urlparse
from app.constants import MAX_URL_DISPLAY_LENGTH

def create_short_link():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    code = "".join([random.choice(chars) for _ in range(8)])
    return code

def validate_url(url):
    try:
        result = urlparse(url)
        valid_scheme = result.scheme in {"http", "https"}
        return valid_scheme and result.netloc
    except ValueError:
        return False

def truncate_url(url):
    if len(url) <= MAX_URL_DISPLAY_LENGTH:
        return url
    return url[:MAX_URL_DISPLAY_LENGTH] + "..."
