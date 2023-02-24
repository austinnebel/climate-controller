/**
 * Defines the URLs used to retreive information
 * from the backend. These are creating using environment
 * variables defined in the `.env` file.
 */
import { ServerHostname } from "env";

/** Full URL to the climate data endpoint. */
export const ClimateDataURL = `http://${ServerHostname}/api/data/`;

/** Full URL to the device data endpoint. */
export const DeviceDataURL = `http://${ServerHostname}/api/device/`;

/** Full URL to the climate data websocket endpoint. */
export const ClimateDataWSURL = `ws://${ServerHostname}/ws/currentData/`;
