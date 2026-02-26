from dataclasses import dataclass, field
from datetime import datetime

from src.app.agent.domain.value_objects.digest_section import DigestSection


@dataclass
class DailyDigest:
    sections: list[DigestSection] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.utcnow)
