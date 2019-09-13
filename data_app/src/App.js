import React from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import Api_retrieval from './components/api_retrieval';

class App extends React.Component {
  render() {
  return (
    <div className="App">
      <div>
        <Api_retrieval />
      </div>
    </div>
  );
}
}


export default App;
