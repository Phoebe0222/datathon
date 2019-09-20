import React, { Component } from 'react';

import DatePicker from "react-datepicker";
 
import "react-datepicker/dist/react-datepicker.css";
import Gun from 'gun/gun';
require('gun/sea');
const fs = require("fs")
export default class Gundb_demo extends React.Component {
		// let gun_val = Gun.get();
		componentDidMount() {
			console.log(Gun.get(123));
	}
	render(){
		return(
			<p>It works!</p>
			);
	}
	}