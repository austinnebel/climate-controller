import { ClimateData } from "hooks/useAPI";
import React from "react";
import DataGraph from "./DataGraph";
import LoadingIndicator from "./LoadingIndicator";

export const GraphContainer = ({ data }: { data?: ClimateData[] }) => {
    if (!data?.length) {
        return <LoadingIndicator />;
    }
    return (
        <>
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
        </>
    );
};

export default GraphContainer;
