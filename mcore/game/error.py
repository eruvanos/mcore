import traceback


def log_err(f):
    """
    Decorator to log errors that would be hidden by pyglet's dispatcher
    """

    # arcade callbacks: wraps does not work here, don't get it
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AttributeError:
            traceback.print_exc()
            raise

    return wrapped
