class BaseTicketBackend:
    """Base class for ticket backend implementations."""

    def __init__(self, **kwargs):
        pass

    def client(self):
        """Return the backend's client.

        :return: The backend's client.
        """
        raise NotImplementedError('subclasses of BaseTicketBackend must implement client')

    def get_poker_stories(self, *args, **kwargs):
        """Get (filtered) stories from the backend.

        :return: A list of dicts. Each dict contains information about a story's ticket number and title.
        :rtype: list[dict]
        """
        raise NotImplementedError('subclasses of BaseTicketBackend must implement get_unpokered_stories.')

    def set_story_points(self, story, *args, **kwargs):
        """Write the pokered story points back to the backend.

        :param planning_poker.models.Story story: The story for which the story points should be written back to the
                                                  backend.
        """
        raise NotImplementedError('subclasses of BaseTicketBackend must implement set_story_points.')

    def get_story_url(self, story):
        """Get the story's url to view it inside a browser.

        :param planning_poker.models.Story story: The story for which the url should be returned.
        :return: The url to the story inside the ticket backend.
        :rtype: str
        """
        raise NotImplementedError('subclasses of BaseTicketBackend must implement get_story_url.')
