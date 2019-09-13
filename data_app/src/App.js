import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
// import bootstrap from 'bootstrap';
// import './Users/shwetha/data_app/node_modules/bootstrap/dist/css/bootstrap.min.css';
import Api_retrieval from './components/api_retrieval';

class App extends React.Component {
  render() {
  return (
    <Router>
    <div className="App">
      <div>
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"></span>
            </button>
            <Link to={'/'} className="navbar-brand">DATA App </Link>
            <div className="collapse navbar-collapse" id="navbarSupportedContent">
              <ul className="navbar-nav mr-auto">
              <li className="nav-item">
                  <Link to={'/'} className="nav-link">Data Retrieval</Link>
                </li>
                <li className="nav-item">
                  <Link to={'/'} className="nav-link">Data Display</Link>
                </li>
                // <li className="nav-item">
                //   <Link to={'/'} className="nav-link">Chat</Link>
                // </li>
                // <li className="nav-item">
                //   <Link to={'/'} className="nav-link">Home</Link>
                // </li>
              </ul>
            </div>
            <button>
              <Link to={'/Api_retrieval'} className="nav-link">Link to Json output</Link>
            </button>
          </nav>
           <Api_retrieval />
      </div>
    </div>
    </Router>
  );
}
}


export default App;
// <div class="dropdown">
// <Api_retrieval />
//   <button class="dropbtn">Dropdown</button>
//   <div class="dropdown-content">
//   <a href="#">Link 1</a>
//   <a href="#">Link 2</a>
//   <a href="#">Link 3</a>
//   </div>
// </div>
