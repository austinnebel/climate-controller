import { Container, Typography } from "@mui/material";
import { ClimateData } from "api/types";
import { AppSection, LoadingIndicator } from "components";
import { formatDate } from "utils";

/**
 * Displays an overview of the current climate data.
 */
export const DataOverviewSection = ({ data }: { data: ClimateData[] }) => {
    let latest = undefined;
    if (data.length > 0) {
        latest = data[data.length - 1];
    }

    if (!latest) {
        return <LoadingIndicator />;
    }

    const temp = (Math.round(latest.temperature * 100) / 100).toFixed(2) + "°F";
    const humidity = (Math.round(latest.humidity * 100) / 100).toFixed(2) + "%";

    return (
        <AppSection heading="Climate">
            <Container
                style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                }}
            >
                <Typography variant="h3">{temp}</Typography>
                <Typography variant="h3">{humidity}</Typography>
                <Typography variant="body1">
                    {formatDate(latest.time)}
                </Typography>
            </Container>
        </AppSection>
    );
};
