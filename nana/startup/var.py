import os
from nana.config import Development as Config

def get_var(name, default=None):
    ENV = bool(os.environ.get('ENV', False))
    if ENV:
        return os.environ.get(name, default)
    else:
        try:
            return getattr(Config, name)
        except AttributeError:
            return None
