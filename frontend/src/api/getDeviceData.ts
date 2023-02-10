import { DeviceData } from "api/types";
import { DeviceDataURL } from "api/urls";
import axios from "axios";

/**
 * Retrieves device data from the backend server.
 */
export const getDeviceData = async () => axios.get<DeviceData[]>(DeviceDataURL);
