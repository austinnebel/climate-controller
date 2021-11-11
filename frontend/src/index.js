import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import { useState, useEffect } from "react";
import { VictoryChart, VictoryLine, VictoryAxis, VictoryTheme } from "victory";
import "./index.css";

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
        console.log(this.props.name);
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
                        tickFormat={(x) => {
                            return new Date(x).toLocaleTimeString([], {
                                hour: "2-digit",
                                minute: "2-digit",
                            });
                        }}
                    />
                </VictoryChart>
            </div>
        );
    }
}

class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            climateData: [],
            deviceData: [],
        };
    }

    async fetchData() {
        try {
            let climateData = await axios.get(
                "http://nebelaustin.tplinkdns.com:4585/api/data/"
            );
            let deviceData = await axios.get(
                "http://nebelaustin.tplinkdns.com:4585/api/device/"
            );

            climateData = climateData.data;
            deviceData = deviceData.data;

            this.setState({
                climateData: climateData,
                deviceData: deviceData,
            });

            console.log("State:" + this.state.climateData.length);
        } catch (e) {
            console.log(e);
        }
    }

    componentDidMount() {
        this.fetchData();
        this.interval = setInterval(() => this.fetchData(), 60000);
    }
    componentWillUnmount() {
        clearInterval(this.interval);
    }

    getCurrentData(dataList) {
        if (dataList.length > 0) {
            let latest = dataList[dataList.length - 1];
            latest.time = new Date(latest.time).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            });
            return latest;
        }
        return {
            temperature: "",
            humidity: "",
            time: "",
        };
    }

    render() {
        let data = this.state.climateData.slice();
        let currData = this.getCurrentData(data);

        return (
            <div className="container">
                <div className="header">
                    <h1>Terrarium</h1>
                </div>
                <h1 className="contentheader">Climate</h1>
                <p className="infoheader">{currData.temperature + "°F"}</p>
                <p className="infoheader">{currData.humidity + "%"}</p>
                <p className="infosubheader">{currData.time}</p>
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
