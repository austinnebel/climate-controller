/**
 * This module exports a set of variables read from
 * the `.env` file.
 */

/**
 * The hostname of the backend server.
 */
export const ServerHostname = process.env.REACT_APP_SERVER_HOSTNAME;

/**
 * The endpoint on the server that retrieves climate data.
 */
export const ClimateDataEndpoint = process.env.REACT_APP_CLIMATE_DATA_ENDPOINT;

/**
 * The endpoint on the server that retrieves device data.
 */
export const DeviceDataEndpoint = process.env.REACT_APP_DEVICE_DATA_ENDPOINT;

/**
 * The endpoint on the server that connects to the climate data websocket.
 */
export const ClimateDataWSEndpoint =
    process.env.REACT_APP_CLIMATE_DATA_WS_ENDPOINT;
