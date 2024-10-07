from enum import Enum

class PatronStatusEnum(Enum):
    AC = "active" # when patron has library books in possession
    IN = "inactive" # when patron has no library books in posession
    SU = "suspended" # when patron has been suspended due to violation of rules
    DE = "deleted" # when patron has been deleted from the system (soft deletion)

class CopyStatusEnum(Enum):
    AV = "available" # when the copy has not been borrowed and is within library premises
    UN = "unavailable but not overdue" # when the copy has been borrowed but is not overdue as of yet
    UO = "unavailable and overdue" # when the copy has been borrowed and is overdue
    RE = "removed" # when the copy has been removed from the system (soft deletion)