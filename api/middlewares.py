from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_apispec import validation_middleware


def get_middlewares(config):
    """Get middlewares for platform application."""
    middlewares = (
        # First, normalize request path, which may result in redirect
        normalize_path_middleware(append_slash=True, merge_slashes=True),
        # After, enable error middleware to catch all errors from any code below
        # error_middleware,
        # Validate API requests
        validation_middleware,
    )
    return middlewares
