from enum import Enum

class PatronStatusEnum(Enum):
    AC = "active"
    IN = "inactive"

class CopyStatusEnum(Enum):
    RE = "retained"
    BD = "borrowed"
    OD = "overdue"