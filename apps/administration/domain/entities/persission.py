from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Permission:
    id: UUID = field(default_factory=uuid4)
    code: str  # ex: "administration:gerer_agences"
    description: str
    module_code: str  # lien vers le module