import { useCallback, useEffect, useState } from "react";

/**
 * Connects a websocket to `url` and returns data of type `T`
 * each time a message is received on it's channel.
 *
 * This will attempt to keep the websocket alive i.e. if the connection fails,
 * a new connection attempt will be made after 10 seconds.
 */
export const useWebsocket = <T>(url: string) => {
    const [socket, setSocket] = useState<WebSocket>();
    const [data, setData] = useState<T>();

    /**
     * Creates a websocket to `url`.
     */
    const create = useCallback(() => new WebSocket(url), [url]);

    /**
     * Called when the websocket unexpectedly closes. This will try to
     * reopen the socket after 10 seconds.
     */
    const onClose = useCallback(
        (e: CloseEvent) => {
            console.error("Webocket closed unexpectedly. ", e);
            setTimeout(() => setSocket(create()), 10000);
        },
        [create]
    );

    /**
     * Called when the websocket receives a message. This automatically parses the text
     * received into JSON.
     */
    const onMessage = useCallback((message: MessageEvent) => {
        const data = JSON.parse(message.data);
        if (!data || data.type !== "send.json") {
            return;
        }
        setData(data.text);
    }, []);

    /**
     * Registers event handlers to the websocket each time
     * it changes. All event handlers are removed during cleanup.
     */
    useEffect(() => {
        if (!socket) return;

        socket.addEventListener("close", onClose);
        socket.addEventListener("message", onMessage);
        socket.addEventListener("error", (e) => {});

        return () => {
            // remove event listeners and close
            socket.removeEventListener("close", onClose);
            socket.removeEventListener("message", onMessage);
        };
    }, [socket, onClose, onMessage]);

    /**
     * Creates the socket on each update to `url` and updates state.
     * The socket is closed during cleanup.
     */
    useEffect(() => {
        const socket = create();
        setSocket(socket);

        return socket.close;
    }, [create]);

    return data;
};
