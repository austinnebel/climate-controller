import axios from "axios";
import { useCallback, useEffect, useRef, useState } from "react";

export type ClimateData = {
    /** Time of data capture. */
    time: string;
    /** Recorded temperature. */
    temperature: number;
    /** Humidity levels in percentage. */
    humidity: number;
};

export const useAPI = (server: string) => {
    const [climateData, setClimateData] = useState<ClimateData[]>([]);
    const [deviceData, setDeviceData] = useState<any[]>([]);
    const dataWS = useRef<WebSocket>();

    /**
     * Initializes a websocket connection to the server and updates the state.
     */
    const initSocket = useCallback(() => {
        dataWS.current = new WebSocket(`ws://` + server + `/ws/currentData/`);
        dataWS.current.onmessage = (e) => {
            const data = JSON.parse(e.data);
            if (!data || data.type !== "send.json") {
                return;
            }
            setClimateData([...climateData, data.text]);
        };

        // reconnects after 10 seconds
        dataWS.current.onclose = (e) => {
            console.error("Chat socket closed unexpectedly.");
            setTimeout(() => {
                initSocket();
            }, 10000);
        };
    }, [server, climateData]);

    // fetch data history on mount. Socket will update afterwards
    useEffect(() => {
        axios
            .get("http://" + server + "/api/data/")
            .then((data) => {
                if (data.status === 200) {
                    setClimateData(data.data as ClimateData[]);
                }
            })
            .catch((err) => {
                console.log(err);
            });

        axios
            .get("http://" + server + "/api/device/")
            .then((data) => {
                if (data.status === 200) {
                    setDeviceData(data.data);
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }, [server]);

    // initializes the websocket and closes it on unmount
    useEffect(() => {
        initSocket();

        return () => {
            if (!dataWS.current) return;

            dataWS.current.onclose = null;
            dataWS.current.close();
        };
    }, [initSocket]);

    return {
        climateData,
        deviceData,
    };
};
