import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import axios from "axios";

import { VictoryChart, VictoryLine, VictoryAxis, VictoryTheme } from "victory";

function Graph(props) {
    if (props.dataPoints === undefined || props.dataPoints.length === 0) {
        return null;
    }
    return (
        <div className="graph">
            <p className="graphheader">{props.name}</p>

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
                    data={props.dataPoints}
                    interpolation="catmullRom"
                    x={props.x}
                    y={props.y}
                    name={props.name}
                />
                <VictoryAxis
                    dependentAxis={true}
                    domain={[60, 100]}
                    tickFormat={(x) => x + props.suffix}
                />
                <VictoryAxis
                    fixLabelOverlap
                    tickFormat={(x) => {
                        let split = x.toString().split(" ");
                        let time = split[1];
                        let AmPm = split[2];
                        let noSeconds =
                            time.split(":")[0] + ":" + time.split(":")[1];
                        return noSeconds + AmPm;
                    }}
                />
            </VictoryChart>
        </div>
    );
}

class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            climateData: [],
        };
    }
    async componentDidMount() {
        try {
            const res = await axios.get(
                "http://nebelaustin.tplinkdns.com:4585/data/api/"
            );
            const climateData = await res.data;

            this.setState({
                climateData: climateData,
            });

            console.log("State:" + this.state);
        } catch (e) {
            console.log(e);
        }
    }
    render() {
        let data = this.state.climateData.slice();
        let temp, humidity, time;
        let temps = [];
        let hums = [];
        let times = [];
        let points = [];
        if (data.length > 0) {
            temp = data[data.length - 1].temperature;
            humidity = data[data.length - 1].humidity;
            time = data[data.length - 1].time;

            let s = time.split(" ");
            if (s.length === 3) {
                time = s[1] + s[2];
            }
        } else {
            temp = humidity = time = "";
        }

        return (
            <div className="container">
                <div className="header">
                    <h1>Terrarium</h1>
                </div>
                <h1 className="contentheader">Climate</h1>
                <p className="infoheader">{temp + "°F"}</p>
                <p className="infoheader">{humidity + "%"}</p>
                <p className="infosubheader">{time}</p>
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
