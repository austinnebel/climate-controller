import { Container, Typography, useTheme } from "@mui/material";
import { formatDate } from "utils";
import {
    VictoryChart,
    VictoryTheme,
    VictoryAxis,
    VictoryLine,
    VictoryScatter,
} from "victory";
import LoadingIndicator from "./LoadingIndicator";

/**
 * Displays a graph of various data types.
 *
 * The type parameter `T` is what data will be shown in the graph.
 * It is the same type that each element in the `data` prop should be.
 */
export const DataGraph = <T extends Record<string, any>>({
    x,
    y,
    data,
    suffix,
    name,
}: {
    /** Data objects to graph. */
    data: T[];
    /** Key in `T` to be used as the x-axis. */
    x: keyof T extends string ? keyof T : never;
    /** Key in `T` to be used as the y-axis. */
    y: keyof T extends string ? keyof T : never;
    /** Suffix to add to y-axis elements, */
    suffix: string;
    /** Graph display name. */
    name: string;
}) => {
    const theme = useTheme();

    if (!data || data.length === 0) {
        return <LoadingIndicator />;
    }

    const convertTimes = data.map((elem) => {
        return {
            ...elem,
            time: new Date(elem.time),
        };
    });

    return (
        <Container style={{ padding: 0 }}>
            <Typography className="graphheader" style={{ textAlign: "center" }}>
                {name}
            </Typography>

            <VictoryChart
                theme={VictoryTheme.material}
                padding={{ top: 5, bottom: 60, left: 50, right: 5 }}
                domainPadding={{ x: [0, 0], y: [10, 10] }}
                domain={{ y: [50, 100] }}
                scale={{ x: "time", y: "linear" }}
                animate={{
                    duration: 500,
                }}
            >
                <VictoryAxis
                    dependentAxis={true}
                    tickFormat={(x) => x + suffix}
                />
                <VictoryAxis fixLabelOverlap={true} tickFormat={formatDate} />

                <VictoryLine
                    style={{
                        data: { stroke: theme.palette.primary.main },
                    }}
                    data={convertTimes}
                    interpolation="catmullRom"
                    x={x}
                    y={y}
                    animate={{
                        duration: 250,
                        easing: "expInOut",
                    }}
                />

                <VictoryScatter
                    style={{
                        data: { fill: theme.palette.primary.main },
                    }}
                    data={[convertTimes[convertTimes.length - 1]]}
                    x={x}
                    y={y}
                    animate={{
                        duration: 250,
                        easing: "expInOut",
                    }}
                />
            </VictoryChart>
        </Container>
    );
};

export default DataGraph;
