from contextlib import contextmanager
from os import environ

@contextmanager
def with_env(**kwargs):
    """
    Set environment variables during the execution.
    import os
    
    with with_env(test="TRUE"):
        print(os.get_env("test")) # -> TRUE
    
    print(os.get_env("test")) # -> None
    """
    origin_env = dict(environ)

    for key, value in kwargs.items():
        if value:
            environ[key] = value
        else:
            del environ[key]

    yield environ

    for key in kwargs.keys():
        value = origin_env.get(key)
        if value:
            environ[key] = value
        else:
            del environ[key]
