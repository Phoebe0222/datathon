import React, { Component } from 'react';
// import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';

// import Gun from 'gun/gun';
// require('gun/sea');

export default class Maps_poly extends Component {
	componentDidMount () {
	    const script = document.createElement("script");

	    script.src = "/Users/shwetha/Practice code/gmaps/gmaps.js";
	    script.async = true;

	    document.body.appendChild(script);
	   //  var map = new GMaps({
    //   					el: '#map',
    //   					lat: 44.490,
    //   					lng: -78.443
    // 				});
    // // 44.599,
    // //       south: 44.490,
    // //       east: -78.443,
    // //       west: -78.649
    // 				var path = [[-78.443,44.490], [-78.443,44.490], [-78.443,44.490],	[-78.443,44.490]];

				// 	polygon = map.drawPolygon({
  		// 				paths: path, // pre-defined polygon shape
				// 		strokeColor: '#BBD8E9',
				// 		strokeOpacity: 1,
				// 		strokeWeight: 3,
				// 		fillColor: '#BBD8E9',
				// 		fillOpacity: 0.6 ,
				// 		editable: true
				// 	});
	}

	render(){

      return (
  				<div id="map">
  				</div>
           );
    	}
    
  }
  