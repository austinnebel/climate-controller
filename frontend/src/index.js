import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import axios from "axios";

import { VictoryChart, VictoryLine, VictoryTheme } from "victory";

/*const data = [
    { quarter: 1, earnings: 13000 },
    { quarter: 2, earnings: 16500 },
    { quarter: 3, earnings: 14250 },
    { quarter: 4, earnings: 19000 },
];*/

function Graph(props) {
    return (
        <VictoryChart theme={VictoryTheme.material}>
            <VictoryLine
                style={{
                    data: { stroke: "#c43a31" },
                    parent: { border: "1px solid #ccc" },
                }}
                data={props.dataPoints}
                x={props.x}
                y={props.y}
            />
        </VictoryChart>
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
            const res = await axios.get("http://localhost:8000/data/");
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
        return (
            <div className="container">
                <div className="header">
                    <h1>Terrarium</h1>
                </div>
                <div className="content">
                    <Graph
                        dataPoints={this.state.climateData}
                        x="time"
                        y="temperature"
                    />
                    <Graph
                        dataPoints={this.state.climateData}
                        x="time"
                        y="humidity"
                    />
                </div>
            </div>
        );
    }
}

// ========================================

ReactDOM.render(<Home />, document.getElementById("root"));
