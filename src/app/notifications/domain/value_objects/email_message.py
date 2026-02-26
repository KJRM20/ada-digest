from dataclasses import dataclass


@dataclass(frozen=True)
class EmailMessage:
    subject: str
    html_body: str
    plain_body: str
    recipient: str
