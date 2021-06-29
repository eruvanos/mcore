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
    for key, value in kwargs.items():
        environ[key] = value

    yield environ

    for key in kwargs.keys():
        del environ[key]
