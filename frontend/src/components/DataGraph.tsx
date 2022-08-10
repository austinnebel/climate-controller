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

type DataGraphProps = {
    /** Key in `data` to be used as the x-axis. */
    x: string;
    /** Key in `data` to be used as the y-axis. */
    y: string;
    /** Data objects to graph. */
    data: any[];
    /** Suffix to add to y-axis elements, */
    suffix: string;
    /** Graph display name. */
    name: string;
};
/**
 * Displays a graph of various data types.
 */
export const DataGraph = ({ x, y, data, suffix, name }: DataGraphProps) => {
    const theme = useTheme();

    if (!data.length) {
        return <LoadingIndicator />;
    }

    return (
        <Container>
            <Typography className="graphheader">{name}</Typography>

            <VictoryChart
                theme={VictoryTheme.material}
                padding={{ top: 5, bottom: 60, left: 50, right: 5 }}
                domainPadding={{ x: [1000, 0], y: [10, 10] }}
                domain={{ y: [60, 100] }}
                scale={{ x: "time", y: "linear" }}
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
                    data={data}
                    interpolation="catmullRom"
                    x={x}
                    y={y}
                    animate={{
                        duration: 300,
                        easing: "expInOut",
                    }}
                />

                <VictoryScatter
                    style={{
                        data: { fill: theme.palette.primary.main },
                    }}
                    data={[data[data.length - 1]]}
                    x={x}
                    y={y}
                    animate={{
                        duration: 300,
                        easing: "expInOut",
                    }}
                />
            </VictoryChart>
        </Container>
    );
};

export default DataGraph;
