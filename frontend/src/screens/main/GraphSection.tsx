import { ClimateData } from "api/types";
import { AppSection, DataGraph } from "components";

export const DataGraphSection = ({ data }: { data: ClimateData[] }) => {
    return (
        <AppSection heading="History">
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
