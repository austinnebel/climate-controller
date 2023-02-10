import { useClimateData } from "api/hooks";
import { DataOverviewSection } from "screens/main/DataOverviewSection";
import { DataGraphSection } from "screens/main/GraphSection";

const SERVER = "127.0.0.1:8000";

export const MainScreen = () => {
    const [climateData, loading] = useClimateData();

    return (
        <AppContainer>
            <DataOverviewSection data={climateData} />
            <DataGraphSection data={climateData} />
        </AppContainer>
    );
};
