from .template import beacon
import praw
from praw.util.token_manager import FileTokenManager


class reddit(beacon):
    def __init__(self, params):
        """
        Initialize a reddit API instance with params
        """
        self.params = params
        self.manager = FileTokenManager(params["token_file"])

        self.reddit = praw.Reddit(
            client_id=self.params["client_id"],
            client_secret=self.params["client_secret"],
            token_manager=self.manager,
            user_agent=self.params["user_agent"],
        )

    def send(self, target, subject, message):
        """
        Send a message using reddit's API
        """
        print(self.reddit.redditor(target)
                          .message(subject, message))
        return 0

    def receive(self):
        return "Reddit received"
