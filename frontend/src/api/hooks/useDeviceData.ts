import { useFetch } from "api/hooks/useFetch";
import { DeviceData } from "api/types";
import { DeviceDataURL } from "api/urls";

export const useDeviceData = (onError?: (reason: any) => void) => {
    /** Fetches device information history. */
    return useFetch<DeviceData[]>(DeviceDataURL, [], onError);
};
