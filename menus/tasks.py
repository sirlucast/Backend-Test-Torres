from celery import shared_task

from menus import helpers


@shared_task(
    name="post_to_user_slack_task",
)
def post_to_user_slack_task(slack_user, attachment, fallback):
    """ Task: Send asynchronously a message to specific employee username using his Slack user ID"""
    helpers.post_to_user_slack(
        username=slack_user, attachment=attachment, fallback=fallback
    )
