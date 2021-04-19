import logging

from django.conf import settings

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def post_to_user_slack(username, message, attachment=None):
    """Send a message to specific username using the slack user ID"""
    client = WebClient(token=settings.SLACK_BOT_TOKEN)
    try:
        client.chat_postMessage(
            channel=username,
            text=message,
            attachments=attachment,
            as_user=True,
        )
    except SlackApiError as e:
        # get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found', etc
        print(f"SLACK SDK got an error: {e.response['error']}")
        if settings.DEBUG:
            logger = logging.getLogger("console")
            logger.error(e.response["error"])
