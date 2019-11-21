import React from 'react';
import ReactDOM from 'react-dom';
import { createBrowserHistory } from "history";
import { Router, Route, Switch, Redirect } from "react-router-dom";

import UserLayout from "./layouts/User";
import * as serviceWorker from './serviceWorker';
import "./assets/css/datathon.css";
import "./assets/css/mapbox.css";

const hist = createBrowserHistory();

ReactDOM.render(
    <Router history={hist}>
        <Switch>
            <Route path="/user" render={props => <UserLayout {...props} />} />
            <Redirect from="/" to="/user/dashboard" />
        </Switch>
    </Router >,
    document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();