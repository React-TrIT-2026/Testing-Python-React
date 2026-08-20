from __future__ import annotations

from dataclasses import dataclass

from studio.domain.models import Plan

PEAK_HOURS = range(18, 22)
LAST_HOUR_OF_DAY = 23
PEAK_SURCHARGE_CENTS = 200
OFF_PEAK_DISCOUNT_CENTS = 100
LOYALTY_TIERS = ((50, 15), (20, 10), (5, 5))


@dataclass(frozen=True, slots=True)
class PriceBreakdown:
    base_cents: int
    surcharge_cents: int
    discount_cents: int

    @property
    def total_cents(self) -> int:
        return max(0, self.base_cents + self.surcharge_cents - self.discount_cents)


def loyalty_discount_percent(classes_attended: int) -> int:
    if classes_attended < 0:
        raise ValueError("Attended classes cannot be negative")
    for threshold, percent in LOYALTY_TIERS:
        if classes_attended >= threshold:
            return percent
    return 0


def is_peak(hour: int) -> bool:
    if not 0 <= hour <= LAST_HOUR_OF_DAY:
        raise ValueError("Hour must be between 0 and 23")
    return hour in PEAK_HOURS


def price_for(base_cents: int, hour: int, plan: Plan, classes_attended: int = 0) -> PriceBreakdown:
    if base_cents < 0:
        raise ValueError("Base price cannot be negative")
    if plan is not Plan.PAY_PER_CLASS:
        return PriceBreakdown(0, 0, 0)

    surcharge = PEAK_SURCHARGE_CENTS if is_peak(hour) else 0
    off_peak = 0 if is_peak(hour) else OFF_PEAK_DISCOUNT_CENTS
    loyalty = base_cents * loyalty_discount_percent(classes_attended) // 100
    return PriceBreakdown(base_cents, surcharge, off_peak + loyalty)
