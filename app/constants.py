# Attempts to shorten a link before returning error
# This is meant to handle the event of a short code collision
SHORTEN_LINK_RETRY_ATTEMPTS = 10

# Regex for verifying user registration fields
USER_FIELD_REGEX = "^[a-zA-Z0-9_]{1,25}$"

# Truncate URLs to ensure they are displayed properly
MAX_URL_DISPLAY_LENGTH = 50

# Length of short link codes
SHORT_CODE_LENGTH = 8
