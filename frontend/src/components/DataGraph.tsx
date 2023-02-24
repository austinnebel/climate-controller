import { Typography, useTheme } from "@mui/material";
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
    style,
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
    /** Graph container style. */
    style?: React.CSSProperties;
}) => {
    const theme = useTheme();

    if (!data || data.length === 0) {
        return <LoadingIndicator />;
    }

    /**
     * Converts any "time" keys to `Date` objects.
     * This is required for victory to calculate the time
     * axis properly.
     */
    data = data.map((elem) => {
        if ("time" in elem) {
            return {
                ...elem,
                time: new Date(elem.time),
            };
        }
        return elem;
    });

    return (
        <div
            style={{
                padding: 0,
                paddingRight: 0,
                ...style,
            }}
        >
            <Typography variant="h6" style={{ textAlign: "center" }}>
                {name}
            </Typography>

            <VictoryChart
                theme={VictoryTheme.material}
                padding={{ top: 5, bottom: 60, left: 50, right: 5 }}
                domainPadding={{ x: [0, 0], y: [10, 10] }}
                domain={{ y: [50, 100] }}
                scale={{ x: "time", y: "linear" }}
                width={400}
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
                        data: {
                            stroke: theme.palette.primary.main,
                            opacity: 0.8,
                        },
                    }}
                    data={data}
                    interpolation="catmullRom"
                    samples={5}
                    x={x}
                    y={y}
                    animate={{
                        duration: 250,
                        easing: "expInOut",
                    }}
                />

                <VictoryScatter
                    style={{
                        data: { fill: "red" },
                    }}
                    data={[data[data.length - 1]]}
                    x={x}
                    y={y}
                    animate={{
                        duration: 250,
                        easing: "expInOut",
                    }}
                />
            </VictoryChart>
        </div>
    );
};

export default DataGraph;
