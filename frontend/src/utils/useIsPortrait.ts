import { useMediaQuery } from "react-responsive";

/**
 * Returns true if the screen's orientation is portrait mode.
 */
export const useIsPortrait = () => {
    return useMediaQuery({ orientation: "portrait" });
};
