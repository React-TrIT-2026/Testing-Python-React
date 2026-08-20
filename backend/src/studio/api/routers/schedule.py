from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from studio.api.dependencies import RepositoriesDep, get_schedule_use_case
from studio.api.schemas import BookingOut, ClassOut, MemberOut
from studio.application.get_schedule import GetSchedule
from studio.domain import errors

router = APIRouter(tags=["schedule"])


@router.get("/classes", response_model=list[ClassOut])
def list_classes(
    schedule: Annotated[GetSchedule, Depends(get_schedule_use_case)],
) -> list[ClassOut]:
    return [ClassOut.from_occupancy(o) for o in schedule.execute()]


@router.get("/members", response_model=list[MemberOut])
def list_members(repos: RepositoriesDep) -> list[MemberOut]:
    return [MemberOut.from_domain(m) for m in repos.members.list_all()]


@router.get("/members/{member_id}", response_model=MemberOut)
def get_member(member_id: int, repos: RepositoriesDep) -> MemberOut:
    member = repos.members.get(member_id)
    if member is None:
        raise errors.MemberNotFound()
    return MemberOut.from_domain(member)


@router.get("/members/{member_id}/bookings", response_model=list[BookingOut])
def member_bookings(member_id: int, repos: RepositoriesDep) -> list[BookingOut]:
    if repos.members.get(member_id) is None:
        raise errors.MemberNotFound()
    return [BookingOut.from_domain(b) for b in repos.bookings.for_member(member_id)]
