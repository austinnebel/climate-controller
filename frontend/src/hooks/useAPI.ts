import { ClimateData, DeviceData } from "api/types";
import axios, { AxiosResponse } from "axios";
import { useCallback, useEffect, useState } from "react";

/**
 * Connects a websocket to `url` and calls `onMessage` each time a message
 * is received.
 *
 * This will attempt to keep the websocket alive i.e. if the connection fails,
 * a new connection attempt will be made after 10 seconds.
 */
const useWebsocket = <T>(url: string, onMessage: (data: T) => void) => {
    const [socket, setSocket] = useState<WebSocket>();

    /**
     * Creates a websocket to `url`.
     */
    const create = useCallback(() => new WebSocket(url), [url]);

    /**
     * Called when the websocket unexpectedly closes. This will try to
     * reopen the socket after 10 seconds.
     */
    const _onClose = useCallback(
        (e: CloseEvent) => {
            console.error("Chat socket closed unexpectedly. ", e);
            setTimeout(create, 10000);
        },
        [create]
    );

    /**
     * Called when the websocket receives a message. This automatically parses the text
     * received into JSON.
     */
    const _onMessage = useCallback(
        (message: MessageEvent) => {
            const data = JSON.parse(message.data);
            if (!data || data.type !== "send.json") {
                return;
            }
            onMessage(data.text);
        },
        [onMessage]
    );

    /**
     * Creates the socket on mount, updates state, and adds an `onClose`
     * event listener.
     *
     * On unmount, this removes the `onClose` event listener and closes the socket.
     */
    useEffect(() => {
        const dataSocket = create();
        setSocket(dataSocket);

        // reconnects after 10 seconds
        dataSocket.addEventListener("close", _onClose);
        dataSocket.addEventListener("message", _onMessage);

        return () => {
            dataSocket.removeEventListener("close", _onClose);
            dataSocket.removeEventListener("message", _onMessage);
            dataSocket.close();
        };
    }, [create, _onClose, _onMessage]);

    return socket;
};

/**
 * Fetches data from `url` and calls `onFetch` once data is received,
 * or `onError` if an error occurs.
 */
const useFetch = <T>(
    url: string,
    onFetch: (data: AxiosResponse<T>) => void,
    onError?: (reason: any) => void
) => {
    useEffect(() => {
        axios
            .get(url)
            .then((data) => {
                console.log("Fetched from ", url, data);
                onFetch(data);
            })
            .catch(onError);
    }, [url, onFetch, onError]);
};

/**
 * Returns climate data history as well as real-time climate information.
 */
export const useClimateData = (server: string) => {
    const [climateData, setClimateData] = useState<ClimateData[]>([]);

    /** Fetches climate data history. */
    useFetch<ClimateData[]>(
        `http://${server}/api/data/`,
        useCallback(
            (data) => setClimateData((oldData) => [...oldData, ...data.data]),
            []
        )
    );

    /**
     * Connect to real-time data socket and
     */
    useWebsocket<ClimateData>(
        `ws://${server}/ws/currentData/`,
        useCallback(
            (data) => setClimateData((oldData) => [...oldData, data]),
            []
        )
    );

    return climateData;
};

export const useDeviceData = (server: string) => {
    const [currentDeviceData, setCurrentDeviceData] = useState<any[]>([]);

    /** Fetches device information history. */
    useFetch<DeviceData[]>(
        `http://${server}/api/device/`,
        useCallback((data) => {
            setCurrentDeviceData((oldData) => [...oldData, ...data.data]);
        }, [])
    );

    return currentDeviceData;
};
