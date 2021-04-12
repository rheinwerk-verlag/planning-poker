from django.template.library import Library

from ..backends.ticket import get_ticket_system

register = Library()


@register.filter
def get_url(story):
    """Return the url the given story has inside the ticket backend.

    :param planning_poker.models.Story story: The story, whose url should be returned.
    :return: The url to the story inside the ticket backend.
    """
    backend = get_ticket_system()
    return backend.get_story_url(story) if backend else None
