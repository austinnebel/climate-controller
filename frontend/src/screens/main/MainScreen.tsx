import { Typography } from "@mui/material";
import { useClimateData, useDeviceData } from "api/hooks";
import { LoadingIndicator } from "components";
import { DataOverviewSection } from "screens/main/DataOverviewSection";
import { DataGraphSection } from "screens/main/GraphSection";

export const MainScreen = () => {
    const [climateData, loading] = useClimateData();

    if (loading) {
        return <LoadingIndicator />;
    }
    if (climateData.length === 0) {
        return <Typography>Error fetching data.</Typography>;
    }
    return (
        <>
            <DataOverviewSection data={climateData} />
            <DataGraphSection data={climateData} />
        </>
    );
};
