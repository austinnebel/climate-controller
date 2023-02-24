import { DeviceData } from "api/types";
import { ClimateDataURL } from "api/urls";
import axios from "axios";

/**
 * Retrieves climate data from the backend server.
 */
export const getClimateData = async () =>
    axios.get<DeviceData[]>(ClimateDataURL);
