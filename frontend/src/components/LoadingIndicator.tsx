import { CircularProgress } from "@mui/material";

export const LoadingIndicator = () => {
    return (
        <div style={{ width: "100%", textAlign: "center" }}>
            <CircularProgress />
        </div>
    );
};

export default LoadingIndicator;
