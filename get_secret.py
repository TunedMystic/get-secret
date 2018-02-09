import os
from os.path import abspath, join


# -------------------------------------
# Helper functions
# -------------------------------------

def _secret_dir():
    root_path = abspath(os.sep)
    return join(root_path, 'run', 'secrets')


def _clean_fn(value):
    return value.strip().replace('\n', '').replace('\r', '')


def _raise(should_raise, exception, default):
    if should_raise:
        raise exception
    return default


class CastException(Exception):
    pass


class CleanException(Exception):
    pass


# -------------------------------------
# Get secret function
# -------------------------------------

def get(key, default=None, to_type=str, env=True,
        clean_fn=_clean_fn, exception=False,
        secret_dir=_secret_dir()):
    """
    The `get` function fetches secrets from a
    secret file or from the environment.

    Parameters
    ----------
    key: str
        The name of the secret to be fetched.

    default
        The default value to use if the secret is not found
        or an exception occurs.

    to_type
        The type that you wish to cast the fetched secret to.
        Must be a type or a callable.

    env: bool
        Should the function fallback to env vars?

    clean_fn
        The clean function to be used for cleaning fetched secrets.

    exception: bool
        If an exception is thrown should it be raised?

    secret_dir: str
        The directory to look for secret files.


    Returns
    ----------
    value
        The value of the secret.


    Raises
    ---------
    CastException
        If the function could not cast the value.

    CleanException
        If the function could not clean the value.

    """

    value = None

    try:
        with open(join(secret_dir, key), 'r') as _file:
            value = _file.read()
    except (IOError) as exc:
        if env:
            value = os.environ.get(key)

    if value is None:
        return default

    try:
        if isinstance(value, str):
            value = clean_fn(value)
    except (Exception) as exc:
        return _raise(exception, CleanException(exc), default)

    try:
        if to_type == bool:
            value = value.lower() in ['true']
        elif value is not None:
            value = to_type(value)
    except (TypeError, ValueError) as exc:
        return _raise(exception, CastException(exc), default)

    return value
