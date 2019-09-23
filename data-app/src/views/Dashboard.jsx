import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";

// reactstrap components
import { Card, CardHeader, CardBody, CardTitle, Row, Col } from "reactstrap";
import Mapload from "../components/Map/Mapload";
// import APIRetreival from "../components/Settings/APIRetrieval";

class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            bigChartData: "data1"
        };
    }
    setBgChartData = name => {
        this.setState({
            bigChartData: name
        });
    };
    render() {
        return (
            <>
                <div className="content">
                    <Row>
                        <Col xs="12">
                            <Card className="card-chart">
                                <CardHeader>
                                </CardHeader>
                                <CardBody></CardBody>
                            </Card>
                        </Col>
                    </Row>
                    <Row>
                        <Col xs="12">
                            <Card className="card-chart">
                                <CardHeader>
                                    <CardTitle tag="h4">Map</CardTitle>
                                </CardHeader>
                                <CardBody>
                                    <Mapload />
                                </CardBody>
                            </Card>
                        </Col>
                    </Row>
                    <Row>
                        <Col lg="8">
                            <Card className="card-chart">
                                <CardHeader>
                                    <CardTitle tag="h4">Geo Information</CardTitle>
                                </CardHeader>
                                <CardBody></CardBody>
                            </Card>
                        </Col>
                        <Col lg="4">
                            <Card className="card-chart">
                                <CardHeader>
                                    <CardTitle tag="h4">Meta Data</CardTitle>
                                </CardHeader>
                                <CardBody></CardBody>
                            </Card>
                        </Col>
                    </Row>
                    <Row>
                        <Col lg="12" md="12">
                            <Card className="card-tasks">
                                <CardHeader>
                                </CardHeader>
                                <CardBody></CardBody>
                            </Card>
                        </Col>

                    </Row>
                </div>
            </>
        );
    }
}

export default Dashboard;
