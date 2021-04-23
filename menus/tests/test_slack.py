from django.conf import settings

from slack_sdk import WebClient

from menus import helpers


def test_get_exception_on_post_to_user_slack_fail(caplog):
    """ Test failed Slack Exception using a fake invalid username"""
    caplog.clear()
    helpers.post_to_user_slack(username="fake_username", message="test")
    assert ["channel_not_found"] == [rec.message for rec in caplog.records]


def test_api_calling_code():
    """ Test SLACK API calling code """
    client = WebClient(token=settings.SLACK_BOT_TOKEN)
    api_response = client.api_test()
    assert api_response["ok"]
    assert api_response["args"]["token"] == settings.SLACK_BOT_TOKEN
