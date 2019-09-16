import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
// import logo from './logo.svg';
import './App.css';
// import bootstrap from 'bootstrap';
// import './Users/shwetha/data_app/node_modules/bootstrap/dist/css/bootstrap.min.css';
import Api_retrieval from './components/api_retrieval';
// import Maps_poly from './components/maps_poly';
 import Mapload from './components/mapload';

class App extends React.Component {
  render() {
  return (
    <div>
    <Router>
    <div className="App">
      <div>
      	<ul className="topnav">
 		 	// <li><a className="active" href="map.html">Home</a></li>
  			<li><Link to={'/'}>Extra</Link></li>
			<li className="right" ><Link to={'/Api_retrieval'}>Data Retrieval</Link></li>
       <li className="right"><Link to={'/Mapload'}>Map Load</Link></li>
		</ul>

      </div>
    </div>
    <Switch>
        <Route path='/Api_retrieval' component={ Api_retrieval } />
        <Route path='/Mapload' component={ Mapload } />
    </Switch>
    </Router>
    </div>
  );
}
}


export default App;
// <Route path='/Mapload' component={ Mapload } />