import axios from "axios";
import { useEffect, useState } from "react";

/**
 * Fetches data from `url` and returns a list with two values;
 * the first being the result (or `defaultValue` if no result fetched),
 * and the second being a boolean indicating if the fetch is currently
 * in progress.
 */
export const useFetch = <T>(
    /** The URL to fetch from. */
    url: string,
    /** The default value to return when fetch has not completed or if there is an error. */
    defaultValue: T,
    /** Called when an exception is thrown during the fetch. */
    onError?: (reason: any) => void
) => {
    const [data, setData] = useState<T>(defaultValue);
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        setLoading(true);
        axios
            .get<T>(url)
            .then((data) => setData(data.data))
            .catch(onError)
            .finally(() => setLoading(false));
    }, [url, onError]);

    return [data, loading] as [data: T, loading: boolean];
};
