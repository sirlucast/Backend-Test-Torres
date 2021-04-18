import logging

from django.conf import settings

import slack

TEST_CHANNEL = settings.SLACK_TEST_CHANNEL


def post_to_user_slack(username, message=None, attachment=None):
    """Send a message to specific username using a slack display username or"""
    client = slack.WebClient(token=settings.SLACK_BOT_TOKEN)
    try:
        # Verify slack display's username matches with existing
        # slack member's id
        # request = client.api_call("users.list")
        # if request["ok"]:
        #     for item in request["members"]:
        #         if item["id"] == username:
        #             username = item["id"]
        client.chat_postMessage(
            channel=username,
            text=message,
            attachments=attachment,
            as_user=True,
        )
    except Exception as e:
        # TODO: notify someone this exception
        if settings.DEBUG:
            # Hook into the slack logger
            # logger = logging.basicConfig()
            logger = logging.getLogger("slack")
            logger.setLevel(logging.DEBUG)
            logger.error(e)
