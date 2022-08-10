import { Container, Typography } from "@mui/material";
import { ClimateData } from "hooks/useAPI";
import { formatDate } from "utils";
import LoadingIndicator from "./LoadingIndicator";

/**
 * Displays the most up-to-date data from the server.
 */
export const DataOverview = ({ data }: { data?: ClimateData }) => {
    if (data && Object.keys(data).length) {
        return (
            <Container
                style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                }}
            >
                <Typography variant="h3">{data.temperature + "°F"}</Typography>
                <Typography variant="h3">{data.humidity + "%"}</Typography>
                <Typography variant="body1">{formatDate(data.time)}</Typography>
            </Container>
        );
    } else {
        return <LoadingIndicator />;
    }
};

export default DataOverview;
