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

class Graph extends React.Component {
    render() {
        let data = this.props.dataPoints.slice();
        let latest;
        if (!data.length) {
            return <div />;
        } else {
            latest = Array(1).fill(data[data.length - 1]);
        }

        let currPoint;
        if (latest.length) {
            currPoint = (
                <VictoryScatter
                    style={{
                        data: { fill: "#c43a31" },
                        size: 10,
                    }}
                    data={latest}
                    x={this.props.x}
                    y={this.props.y}
                />
            );
        }

        return (
            <div className="graph">
                <p className="graphheader">{this.props.name}</p>

                <VictoryChart
                    theme={VictoryTheme.material}
                    padding={{ top: 5, bottom: 60, left: 50, right: 50 }}
                    domainPadding={20}
                >
                    <VictoryAxis
                        dependentAxis={true}
                        domain={[60, 100]}
                        tickFormat={(x) => x + this.props.suffix}
                    />
                    <VictoryAxis
                        fixLabelOverlap={true}
                        tickFormat={formatDate}
                    />
                    <VictoryLine
                        style={{
                            data: { stroke: "#c43a31" },
                            parent: { border: "1px solid #ccc" },
                        }}
                        data={data}
                        interpolation="catmullRom"
                        x={this.props.x}
                        y={this.props.y}
                        name={this.props.name}
                    />
                    {currPoint}
                </VictoryChart>
            </div>
        );
    }
}

function DataOverview(props) {
    if (props.data) {
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
            currentInfo: {},
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
            this.setState({ currentInfo: data.text });
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
        // if no data history, return sockInfo
        if (!history) {
            return sockInfo;
        }
        let latestHistory = history[history.length - 1];
        // if sockInfo is undefined, return latest history
        if (!sockInfo.time) {
            if (!latestHistory) {
                return null;
            }
            return latestHistory;
        }

        // get most recent date
        let historyTime = new Date(latestHistory.time);
        let sockTime = new Date(sockInfo.time);

        if (sockTime > historyTime) {
            return sockInfo;
        }
        return latestHistory;
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
        let currData = this.latestInfo(data, this.state.currentInfo);

        console.log(data);

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
                    onUpdate={this.fetchData}
                />
                <Graph
                    dataPoints={data}
                    x="time"
                    y="humidity"
                    name="Humidity"
                    suffix="%"
                    onUpdate={this.fetchData}
                />
            </div>
        );
    }
}

// ========================================

ReactDOM.render(<Home />, document.getElementById("root"));
