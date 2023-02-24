/**
 * Represents a climate data entry from the database.
 */
export type ClimateData = {
    /** Time of data capture. */
    time: string;
    /** Recorded temperature. */
    temperature: number;
    /** Humidity levels in percentage. */
    humidity: number;
};

/**
 * Represents climate data entry from the database.
 */
export type DeviceData = {
    /** Time that `event` occurred. */
    time: string;
    event: string;
    device: string;
};
