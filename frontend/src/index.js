import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import PropTypes from "prop-types";
import { TailSpin } from "react-loading-icons";
import {
    VictoryChart,
    VictoryLine,
    VictoryAxis,
    VictoryTheme,
    VictoryScatter,
} from "victory";
import "./index.css";

const SERVER = "nebelaustin.tplinkdns.com:4585";

/**
 * Parses a Date or string object into a string of format HH:MM AM/PM
 *
 * @param {Date | string} date Parses a Date object into a string of format HH:MM AM/PM
 * @returns string
 */
function formatDate(date) {
    if (date instanceof Date || typeof date === "string") {
        return new Date(date)
            .toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            })
            .replace(/\s+/g, "");
    } else {
        console.log(
            "Received invalid date to format: " +
                date +
                " of type " +
                typeof date
        );
    }
}

/**
 * Converts an objects time property into a Date object.
 *
 * If the object does not have a time property, returns the object.
 *
 * @param {Object} obj Object to evaluate.
 * @returns Object
 */
function parseDate(obj) {
    if ("time" in obj && typeof obj.time === "string") {
        obj.time = new Date(obj.time);
    }
    return obj;
}
function parseAllDates(list) {
    return list.map((i) => parseDate(i));
}

function Loading() {
    return <TailSpin stroke="black" className="graph" />;
}

function Graph(props) {
    const { x, y, dataPoints, suffix, name } = props;

    if (!dataPoints.length) {
        return null;
    }

    console.log("Graphing " + dataPoints.length + " points.");
    const animation = {
        duration: 300,
        easing: "expInOut",
    };
    const lineColor = "#e43124";
    const pointColor = "#eb3124";
    const mostRecent = Array(1).fill(dataPoints[dataPoints.length - 1]);

    return (
        <div className="graph">
            <p className="graphheader">{name}</p>

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
                        data: { stroke: lineColor },
                    }}
                    data={dataPoints}
                    interpolation="catmullRom"
                    x={x}
                    y={y}
                    animate={animation}
                />

                <VictoryScatter
                    style={{
                        data: { fill: pointColor },
                        size: 10,
                    }}
                    data={mostRecent}
                    x={x}
                    y={y}
                    animate={animation}
                />
            </VictoryChart>
        </div>
    );
}
Graph.propTypes = {
    dataPoints: PropTypes.arrayOf(
        PropTypes.shape({
            time: PropTypes.string.isRequired,
            temperature: PropTypes.number.isRequired,
            humidity: PropTypes.number.isRequired,
        })
    ).isRequired,
    x: PropTypes.string,
    y: PropTypes.string.isRequired,
    name: PropTypes.string,
    suffix: PropTypes.string,
};

function DataOverview(props) {
    if (props.data && Object.keys(props.data).length) {
        return (
            <div>
                <p className="infoheader">{props.data.temperature + "°F"}</p>
                <p className="infoheader">{props.data.humidity + "%"}</p>
                <p className="infosubheader">{formatDate(props.data.time)}</p>
            </div>
        );
    } else {
        return <Loading />;
    }
}

function GraphContainer(props) {
    const data = props.data;

    if (data.length > 0) {
        return (
            <div>
                <Graph
                    dataPoints={data}
                    x="time"
                    y="temperature"
                    name="Temperature"
                    suffix="°F"
                />
                <Graph
                    dataPoints={data}
                    x="time"
                    y="humidity"
                    name="Humidity"
                    suffix="%"
                />
            </div>
        );
    } else {
        return <Loading />;
    }
}
class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            climateData: [],
            deviceData: [],
            sockInfo: {},
        };
    }

    async fetchData() {
        try {
            let climateData = await axios.get(
                "http://" + SERVER + "/api/data/"
            );
            let deviceData = await axios.get(
                "http://" + SERVER + "/api/device/"
            );

            climateData = climateData.data;
            deviceData = deviceData.data;

            this.setState({
                climateData: climateData,
                deviceData: deviceData,
            });
        } catch (e) {
            console.log(e);
        }
    }

    initSocket() {
        this.updatesSocket = new WebSocket(
            `ws://` + SERVER + `/ws/currentData/`
        );
        this.updatesSocket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            if (data.type !== "send.json") {
                return;
            }
            this.setState({ sockInfo: data.text });
        };

        // reconnects after 10 seconds
        this.updatesSocket.onclose = (e) => {
            console.error("Chat socket closed unexpectedly.");
            setTimeout(() => {
                this.initSocket();
            }, 10000);
        };
    }

    latestInfo(history, sockInfo) {
        // return sockInfo by default if available
        if (Object.keys(sockInfo).length) {
            return sockInfo;
        }

        // if history also not available, do nothing, return null
        if (!history.length) {
            return null;
        }
        return history[history.length - 1];
    }

    componentDidMount() {
        this.fetchData();
        this.initSocket();

        this.interval = setInterval(() => this.fetchData(), 60000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
        this.updatesSocket.close();
    }

    render() {
        let data = this.state.climateData.slice();
        let currData = this.latestInfo(data, this.state.sockInfo);

        if (currData) {
            data.push(currData);
        }

        return (
            <div className="container">
                <div className="title-background">
                    <h1 className="page-title"> Terrarium</h1>
                </div>

                <h1 className="contentheader">Climate</h1>
                <DataOverview data={currData} />

                <h1 className="contentheader">Statistics</h1>
                <GraphContainer data={data} />
            </div>
        );
    }
}

// ========================================

ReactDOM.render(<Home />, document.getElementById("root"));
