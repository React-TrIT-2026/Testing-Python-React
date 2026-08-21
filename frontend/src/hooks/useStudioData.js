import { useCallback, useEffect, useMemo, useState } from "react";

const EMPTY = { classes: [], members: [], member: null, bookings: [] };

export function useStudioData(api, memberId) {
  const [data, setData] = useState(EMPTY);
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    try {
      const [classes, members] = await Promise.all([api.listClasses(), api.listMembers()]);
      
      const [member, bookings] = memberId
        ? await Promise.all([api.getMember(memberId), api.listBookings(memberId)])
        : [null, []];

      setData({ classes, members, member, bookings });
      setError(null);
      setStatus("ready");
    } catch (caught) {
      setError(caught);
      setStatus("error");
    }
  }, [api, memberId]);

  useEffect(() => {
    load();
  }, [load]);

  const activeBookings = useMemo(
    () =>
      data.bookings.filter((b) => b.status === "confirmed" || b.status === "waitlisted"),
    [data.bookings],
  );

  return { ...data, activeBookings, status, error, reload: load };
}
