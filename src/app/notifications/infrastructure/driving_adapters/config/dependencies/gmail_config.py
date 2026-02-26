from src.app.notifications.infrastructure.driven_adapters.gmail.adapters.simplegmail_adapter import (
    SimplegmailAdapter,
)


def get_gmail_adapter() -> SimplegmailAdapter:
    return SimplegmailAdapter()
