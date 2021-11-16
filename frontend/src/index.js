import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import {
    VictoryChart,
    VictoryLine,
    VictoryAxis,
    VictoryTheme,
    VictoryScatter,
} from "victory";
import "./index.css";

const SERVER = "nebelaustin.tplinkdns.com:4585";

function formatDate(date) {
    return new Date(date)
        .toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
        })
        .replace(/\s+/g, "");
}

function Graph(props) {
    if (!props.dataPoints.length) {
        return <div />;
    }

    console.log("Graphing " + props.dataPoints.length + " points.");
    const animation = {
        duration: 300,
        easing: "expInOut",
    };
    const lineColor = "#c43a31";
    const mostRecent = Array(1).fill(
        props.dataPoints[props.dataPoints.length - 1]
    );

    return (
        <div className="graph">
            <p className="graphheader">{props.name}</p>

            <VictoryChart
                theme={VictoryTheme.material}
                padding={{ top: 5, bottom: 60, left: 50, right: 5 }}
                domainPadding={{ x: [1000, 0], y: [10, 10] }}
                domain={{ y: [60, 100] }}
                scale={{ x: "time", y: "linear" }}
            >
                <VictoryAxis
                    dependentAxis={true}
                    tickFormat={(x) => x + props.suffix}
                />
                <VictoryAxis fixLabelOverlap={true} tickFormat={formatDate} />

                <VictoryLine
                    style={{
                        data: { stroke: lineColor },
                    }}
                    data={props.dataPoints}
                    interpolation="catmullRom"
                    x={props.x}
                    y={props.y}
                    animate={animation}
                />

                <VictoryScatter
                    style={{
                        data: { fill: lineColor },
                        size: 10,
                    }}
                    data={mostRecent}
                    x={props.x}
                    y={props.y}
                    animate={animation}
                />
            </VictoryChart>
        </div>
    );
}

function DataOverview(props) {
    if (props.data && Object.keys(props.data).length) {
        return (
            <div>
                <p className="infoheader">{props.data.temperature + "°F"}</p>
                <p className="infoheader">{props.data.humidity + "%"}</p>
                <p className="infosubheader">{props.data.time}</p>
            </div>
        );
    } else {
        return <div></div>;
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
                <div className="header">
                    <h1>Terrarium</h1>
                </div>
                <h1 className="contentheader">Climate</h1>
                <DataOverview data={currData} />
                <h1 className="contentheader">Statistics</h1>
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
    }
}

// ========================================

ReactDOM.render(<Home />, document.getElementById("root"));
