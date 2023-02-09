import { AppContainer } from "components";
import { useClimateData } from "hooks/useAPI";
import { DataOverviewSection } from "screens/main/DataOverviewSection";
import { DataGraphSection } from "screens/main/GraphSection";

const SERVER = "127.0.0.1:8000";

export const MainScreen = () => {
    const climateData = useClimateData(SERVER);

    return (
        <AppContainer>
            <DataOverviewSection data={climateData} />
            <DataGraphSection data={climateData} />
        </AppContainer>
    );
};
