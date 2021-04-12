from django.conf import settings
from django.utils.module_loading import import_string


def get_ticket_system(backend=None, **kwargs):
    """Return the current ticket backend specified or load it from the settings.

    :param str backend: A dotted path to the backend you want to load.
    The backend specified in the settings will be used if this parameter is omitted, optional.
    :param kwargs: Additional parameters used to call the backend.
    :return: An instance of the specified backend.
    """
    try:
        backend_class = import_string(backend or settings.TICKET_SYSTEM['BACKEND'])
    except (AttributeError, KeyError):
        backend_class = None
    return backend_class(**kwargs) if backend_class else None
