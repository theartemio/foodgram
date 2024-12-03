# Short link code length
MAX_SHORT_LINK_CODE = 3

# Recipe, tag, ingredient constants

# Maximum length for recipe, ingredient and tag names
MAX_NAMES_LENGTH = 256
# Maximum length for slugs
MAX_SLUG_LENGTH = 150

# User constants

# Maximum username, first and last name length
MAX_USER_NAMES_LENGTH = 150

# Username allowed symbols
USERNAME_PATTERN = r"^[\w.@+-]+\Z"

# Maximum length for emails
MAX_EMAIL_LENGTH = 254

# Maximum role length
MAX_ROLE_LENGTH = 16

# Admin role
ADMIN = "admin"

# User role
USER = "user"

# User roles
CHOICES = (
    (USER, USER),
    (ADMIN, ADMIN),
)

# Domain for shortened links
DOMAIN = "https://superfoodgram3000.ddns.net/"
