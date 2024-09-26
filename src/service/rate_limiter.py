from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


# Initialize the Limiter
pt_limiter = Limiter(key_func=get_remote_address)
