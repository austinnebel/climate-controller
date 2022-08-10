import {
    AppContainer,
    AppSection,
    DataOverview,
    GraphContainer,
} from "components";
import { useAPI } from "hooks/useAPI";

//const SERVER = "nebelaustin.tplinkdns.com:4585";
const SERVER = "192.168.1.117:8000";

export const MainScreen = () => {
    const { climateData } = useAPI(SERVER);

    const latestData = climateData?.length
        ? climateData[climateData.length - 1]
        : undefined;

    return (
        <AppContainer>
            <AppSection heading="Climate">
                <DataOverview data={latestData} />
            </AppSection>

            <AppSection heading="History">
                <GraphContainer data={climateData} />
            </AppSection>
        </AppContainer>
    );
};
