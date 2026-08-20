from __future__ import annotations

LOYALTY_THRESHOLD = 20
MAX_FORGIVENESS = 1


def forgives_late_cancellation(classes_attended: int, previous_forgiven: int) -> bool:
    if classes_attended < 0 or previous_forgiven < 0:
        raise ValueError("Counters cannot be negative")
    if previous_forgiven >= MAX_FORGIVENESS:
        return False
    return classes_attended >= LOYALTY_THRESHOLD
