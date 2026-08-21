import { renderHook, waitFor } from "@testing-library/react";
import { HttpReponse, http } from "@msw"

import { createApiClient } from "../../src/api/client";
import { useStudioData } from '../../src/hooks/useStudioData';

const api = createApiClient({ baseUrl: "/api" });

describe("loading the studio", () => {
    it("starts in the loading state", () => {
        const { result } = renderHook( () => useStudioData(api, 1));

        expect(result.current.status).toBe("loading");
        expect(result.current.classes).toEqual([]);
    });

    it("ends up ready with schedule and the member", async () => {
        const { result } = renderHook( () => useStudioData(api, 1));

        await waitFor(() => expect(result.current.status).toBe("ready"));

        for (const session of result.current.classes) {
            expect(new Date(session.start_at) >= new Date(state.now)).toBe(true)
        }
    })

    it("leaves past classes out of the schedule", async () => {
        const { result, rerender } = renderHook(
            ({memberId}) => useStudioData(api, memberId),
            {
                initialProps: { memberId: 1}
            },
        );

        await waitFor(() => expect(result.current.member?.id).toBe(1));

        rerender({ memberId: 2 })

        await waitFor(() => expect(result.current.member?.id).toBe(2));

    })
});

// TODO: Test Level = 5 
// describe("failure", () => {});

// TODO: Test Level = 8
// describe("active bookings", () => {});