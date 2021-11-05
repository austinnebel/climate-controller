import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import axios from "axios";

import { VictoryChart, VictoryLine, VictoryAxis, VictoryTheme } from "victory";

function Graph(props) {
    return (
        <div className="graph">
            <p class="graphheader">{props.name}</p>

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
                    tickValues={props.x}
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
            const res = await axios.get("http://localhost:8000/data/api/");
            const climateData = await res.data;

            this.setState({
                climateData: climateData,
            });

            console.log(this.state);
        } catch (e) {
            console.log(e);
        }
    }
    render() {
        let data = this.state.climateData;
        let temp, humidity, time;
        if (data.length > 0) {
            temp = data[data.length - 1].temperature;
            humidity = data[data.length - 1].humidity;
            time = data[data.length - 1].time;

            let s = time.split(" ");
            console.log(s);
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
                <h1 class="contentheader">Climate</h1>
                <p class="infoheader">{temp + "°F"}</p>
                <p class="infoheader">{humidity + "%"}</p>
                <p class="infosubheader">{time}</p>
                <h1 class="contentheader">Statistics</h1>
                <Graph
                    dataPoints={this.state.climateData}
                    x="time"
                    y="temperature"
                    name="Temperature"
                    suffix="°F"
                />
                <Graph
                    dataPoints={this.state.climateData}
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
