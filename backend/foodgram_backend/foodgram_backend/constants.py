# Maximum length for emails
MAX_EMAIL_LENGTH = 254

# Maximum length for slugs
MAX_SLUG_LENGTH = 150

# Maximum length for names of all kinds
MAX_NAMES_LENGTH = 150

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

# Tuples of methods for limiting viewsets
GET_POST_DELETE = ("get", "post", "delete",)

GET = ("get",)

# Username allowed symbols
USERNAME_PATTERN = r"^[\w.@+-]+\Z"

