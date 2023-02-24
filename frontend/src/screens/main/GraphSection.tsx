import { ClimateData } from "api/types";
import { AppSection, DataGraph } from "components";
import { useIsPortrait } from "utils/useIsPortrait";

export const DataGraphSection = ({ data }: { data: ClimateData[] }) => {
    const isPortrait = useIsPortrait();

    return (
        <AppSection
            heading="History"
            style={{
                display: "flex",
                gap: "24px",
                flexDirection: isPortrait ? "column" : "row",
            }}
        >
            <DataGraph
                data={data}
                x="time"
                y="temperature"
                name="Temperature"
                suffix="°F"
            />
            <DataGraph
                data={data}
                x="time"
                y="humidity"
                name="Humidity"
                suffix="%"
            />
        </AppSection>
    );
};
