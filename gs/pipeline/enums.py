from enum import Enum, auto

class BatchHealth(Enum):
    ok=auto()               # Ready for calculations
    bad=auto()              # Unlabeled frames < labelled frames
    success=auto()          # Completed calculations
    error=auto()            # In case


