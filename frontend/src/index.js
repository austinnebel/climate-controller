import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import { useState, useEffect } from "react";
import { VictoryChart, VictoryLine, VictoryAxis, VictoryTheme } from "victory";
import "./index.css";

const SERVER = "localhost:8000";

function formatDate(date) {
    return new Date(date).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
    });
}

class Graph extends React.Component {
    async componentDidUpdate(prevProps) {
        if (this.props.data !== prevProps.climateData) {
            this.props.fetchData();
        }
    }

    render() {
        let data = this.props.dataPoints.slice();
        if (!data) {
            return null;
        }
        return (
            <div className="graph">
                <p className="graphheader">{this.props.name}</p>

                <VictoryChart
                    theme={VictoryTheme.material}
                    padding={{ top: 5, bottom: 60, left: 50, right: 50 }}
                    domainPadding={20}
                >
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
                    <VictoryAxis
                        dependentAxis={true}
                        domain={[60, 100]}
                        tickFormat={(x) => x + this.props.suffix}
                    />
                    <VictoryAxis
                        fixLabelOverlap={true}
                        tickFormat={formatDate}
                    />
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

        this.updatesSocket.onclose = function (e) {
            console.error("Chat socket closed unexpectedly.");
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
