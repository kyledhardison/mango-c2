from .template import beacon
import praw
from praw.models import Message
from praw.util.token_manager import FileTokenManager


class reddit(beacon):
    def __init__(self, params):
        """
        Initialize a reddit API instance with params
        """
        self.params = params
        self.manager = FileTokenManager(params["token_file"])
        self.target = params["target"]

        self.reddit = praw.Reddit(
            client_id=self.params["client_id"],
            client_secret=self.params["client_secret"],
            token_manager=self.manager,
            user_agent=self.params["user_agent"],
        )

    def send(self, target, subject, message):
        """
        Send a message using reddit's API
        Return 0 is successful
        """
        # NOTE: 10,000 character limit on messages
        try:
            self.reddit.redditor(target).message(subject, message)
        except:
            return 1
        return 0

    def receive(self):
        """
        Receive all unread messages from the inbox, in the order they
        were received

        Returned messages should be accessed with the .pop() method, 
        to keep them in order

        Return an empty list if no messages exist.
        """
        # NOTE: 10,000 character limit on messages
        messages = []
        for m in self.reddit.inbox.unread(limit=None):
            if isinstance(m, Message):
                messages.append(m)
        if not messages:
            return messages
        else:
            self.reddit.inbox.mark_read(messages)
            return [m.body for m in messages]
