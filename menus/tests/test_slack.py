import pytest
from django.conf import settings

from _pytest.outcomes import Failed
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from menus import helpers


def test_get_exception_on_post_to_user_slack_fail():
    """ Test failed Slack Exception using a fake invalid username"""
    try:
        with pytest.raises(SlackApiError):
            helpers.post_to_user_slack("fake_username", "msg")
    except Failed:
        pass


def test_api_calling_code():
    """ Test SLACK API calling code """
    client = WebClient(token=settings.SLACK_BOT_TOKEN)
    api_response = client.api_test()
    assert api_response["ok"]
    assert api_response["args"]["token"] == settings.SLACK_BOT_TOKEN
