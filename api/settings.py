import os
from pathlib import Path
from typing import Optional

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader  # noqa:F401, WPS440


def load_config(path: Path, custom_config: Optional[str] = None) -> dict:
    """Load config from YAML file(s)"""

    # Load default config from api directory
    with open(path.joinpath("api/config.yaml"), "r") as load_file:
        config = load(load_file, Loader=Loader)

    # Load additional config
    if custom_config:
        with open(path.joinpath(custom_config), "r") as load_additional_file:
            additional_config = load(load_additional_file, Loader=Loader)
            # Update default config with additional
            if additional_config:
                config.update(**additional_config)

    # Update config with environment variables
    for env_key in config.keys():
        environ_value = os.environ.get(env_key.upper())
        if environ_value:
            config.update({env_key: environ_value})

    for env_key, env_value in config.items():
        if env_key == "database_uri":
            os.environ[env_key] = env_value

    return config
