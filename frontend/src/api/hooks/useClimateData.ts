import { ClimateData } from "api/types";
import { useFetch } from "api/hooks/useFetch";
import { useWebsocket } from "api/hooks/useWebsocket";
import { useEffect, useState } from "react";
import { ClimateDataURL, ClimateDataWSURL } from "api/urls";

/**
 * Returns climate data history as well as real-time climate information.
 */
export const useClimateData = () => {
    /**
     * A list of climate data objects.
     * This includes history + data points retrieved from the websocket.
     */
    const [climateData, setClimateData] = useState<ClimateData[]>([]);

    /** Fetches climate data history. */
    const [history, loading] = useFetch<ClimateData[]>(ClimateDataURL, []);

    /** Establishes websocket connection. */
    const wsData = useWebsocket<ClimateData>(ClimateDataWSURL);

    /** Adds history to the beggining of `data` once fetched. */
    useEffect(() => {
        setClimateData((data) => [...history, ...data]);
    }, [history]);

    /** Appends websocket data to the end of `data`. */
    useEffect(() => {
        if (!wsData) return;
        setClimateData((data) => [...data, wsData]);
    }, [wsData]);

    return [climateData, loading] as [data: ClimateData[], loading: boolean];
};
