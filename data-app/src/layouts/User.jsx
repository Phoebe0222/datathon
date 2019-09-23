// As a Farmer I want to know how to improve the yield of my crop, including:
// - How I can improve my soil (e.g. pH, nitrogen / phosphorus
// - How I can better time my planting / harvesting
// As a farmer, I want better visibility into how my crop compares to other farmers in the area as it grows
// As a farmer, I want to know what my yield is likely to be at the end of the season

import React from "react";
import { Route, Switch } from "react-router-dom";
// javascript plugin used to create scrollbars on windows
import PerfectScrollbar from "perfect-scrollbar";

// core components
import NavigationBar from "../components/Navbar/NavigationBar";
import Footer from "../components/Footer/Footer";
import Sidebar from "../components/Sidebar/Sidebar";

import routes from "../routes.js";

import logo from "../assets/img/react-logo.png";

var ps;

class User extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            backgroundColor: "blue",
            sidebarOpened:
                document.documentElement.className.indexOf("nav-open") !== -1
        };
    }
    componentDidMount() {
        if (navigator.platform.indexOf("Win") > -1) {
            document.documentElement.className += " perfect-scrollbar-on";
            document.documentElement.classList.remove("perfect-scrollbar-off");
            ps = new PerfectScrollbar(this.refs.mainPanel, { suppressScrollX: true });
            let tables = document.querySelectorAll(".table-responsive");
            for (let i = 0; i < tables.length; i++) {
                ps = new PerfectScrollbar(tables[i]);
            }
        }
    }
    componentWillUnmount() {
        if (navigator.platform.indexOf("Win") > -1) {
            ps.destroy();
            document.documentElement.className += " perfect-scrollbar-off";
            document.documentElement.classList.remove("perfect-scrollbar-on");
        }
    }
    componentDidUpdate(e) {
        if (e.history.action === "PUSH") {
            if (navigator.platform.indexOf("Win") > -1) {
                let tables = document.querySelectorAll(".table-responsive");
                for (let i = 0; i < tables.length; i++) {
                    ps = new PerfectScrollbar(tables[i]);
                }
            }
            document.documentElement.scrollTop = 0;
            document.scrollingElement.scrollTop = 0;
            this.refs.mainPanel.scrollTop = 0;
        }
    }
    // this function opens and closes the sidebar on small devices
    toggleSidebar = () => {
        document.documentElement.classList.toggle("nav-open");
        this.setState({ sidebarOpened: !this.state.sidebarOpened });
    };
    getRoutes = routes => {
        return routes.map((prop, key) => {
            if (prop.layout === "/user") {
                return (
                    <Route
                        path={prop.layout + prop.path}
                        component={prop.component}
                        key={key}
                    />
                );
            } else {
                return null;
            }
        });
    };
    handleBgClick = color => {
        this.setState({ backgroundColor: color });
    };
    getBrandText = path => {
        for (let i = 0; i < routes.length; i++) {
            if (
                this.props.location.pathname.indexOf(
                    routes[i].layout + routes[i].path
                ) !== -1
            ) {
                return routes[i].name;
            }
        }
        return "Brand";
    };
    render() {
        return (
            <>
                <div className="wrapper">
                    <Sidebar
                        {...this.props}
                        routes={routes}
                        bgColor={this.state.backgroundColor}
                        logo={{
                            outterLink: "https://www.creative-tim.com/",
                            text: "Datathon",
                            imgSrc: logo
                        }}
                        toggleSidebar={this.toggleSidebar}
                    />
                    <div
                        className="main-panel"
                        ref="mainPanel"
                        data={this.state.backgroundColor}
                    >
                        <NavigationBar
                            {...this.props}
                            brandText={this.getBrandText(this.props.location.pathname)}
                            toggleSidebar={this.toggleSidebar}
                            sidebarOpened={this.state.sidebarOpened}
                        />
                        <Switch>{this.getRoutes(routes)}</Switch>
                        {// we don't want the Footer to be rendered on map page
                            this.props.location.pathname.indexOf("maps") !== -1 ? null : (
                                <Footer fluid />
                            )}
                    </div>
                </div>
            </>
        );
    }
}

export default User;
