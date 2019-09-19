import React, { Component } from 'react';

import DatePicker from "react-datepicker";
 
import "react-datepicker/dist/react-datepicker.css";
import Gun from 'gun/gun';
require('gun/sea');
// import Gundb_demo from './gundb_demo'
const fs = require("fs")
const value = 1;
const display_obj_2_json = 1;
export default class Api_retrieval extends React.Component {
  onClickHandler = () => {
    axios.post("http://localhost:3000", display_obj_2_json, { // receive two parameter endpoint url ,form data 
      })
      .then(res => { // then print response status
        console.log(res.statusText)
      })
}
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: [],
      startDate: new Date()
    };
  }
  handleChange = date => {
    this.setState({
      startDate: date
    });
  };
  componentDidMount() {
    let fetch_val = fetch("https://api.nasa.gov/neo/rest/v1/feed?start_date=2019-09-06&end_date=2019-09-07&&id=2465617&results=1&api_key=KwRDL3x7w75naVBiJua5GmSpMEDn75yNMjMqacS8");
    fetch_val = (fetch_val => fetch_val.json())
    console.log(fetch_val);  
    fetch("https://api.nasa.gov/neo/rest/v1/feed?start_date=2019-09-06&end_date=2019-09-07&&id=2465617&results=1&api_key=KwRDL3x7w75naVBiJua5GmSpMEDn75yNMjMqacS8")
      .then(res => res.json())
      .then(
        (result) => {
          // const first_numeric_key = 2019-09-06;
          // first_numeric_key = first_numeric_key.toString();

          // const val = this.state.startDate;
          // console.log(val);
          const value = 0;
          const val = "2019-09-06";
          const index = "0";
          // document.write(result.near_earth_objects[val][index])
          let display = result.near_earth_objects[val][index];
           // document.getElementById('root').innerHTML += (JSON && JSON.stringify ? JSON.stringify(display) : display) + '<br />';
          display_obj_2_json = (JSON && JSON.stringify ? JSON.stringify(display) : display) ;
          document.getElementById('root').innerHTML += display_obj_2_json;
          // document.write(display_obj_2_json);
          console.log(display)
          let id = 123;
          const gun_display = {
            uuid : id,
            value : display_obj_2_json
          } ;
          var gun = Gun()
          gun.get(123).put(display_obj_2_json)
          console.log(gun)
          // document.getElementById('root').innerHTML = console.log(result.near_earth_objects[val][index]);

          // document.write = result.near_earth_objects[val][index];
          const data_temp = result.near_earth_objects[val][index]
          this.setState({
            isLoaded: true,
            items: result.items
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
 
  }
// (function(console){

//     console.save = function(data, filename){

//         if(!data) {
//             console.error('Console.save: No data')
//             return;
//         }

//         if(!filename) filename = 'console.json'

//         if(typeof data === "object"){
//             data = JSON.stringify(data, undefined, 4)
//         }

//         var blob = new Blob([data], {type: 'text/json'}),
//             e    = document.createEvent('MouseEvents'),
//             a    = document.createElement('a')

//         a.download = filename
//         a.href = window.URL.createObjectURL(blob)
//         a.dataset.downloadurl =  ['text/json', a.download, a.href].join(':')
//         e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
//         a.dispatchEvent(e)
//     }
// })(console)
  render() {
    // if(value == 1){
    //   return <DatePicker selected={this.state.startDate}
    //     onChange={this.handleChange}/>;
    // }
    
    const { error, isLoaded, items } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else{
      return (
        <div>
        <p>Its fetching</p>
         <button onClick = {this.onClickHandler}>Upload</button>
        </div>
      );
    }
  }
}
// .then(data => {
//      let data_val = data.results.map((retr) => {
//        return(
//            <div key={retr.results}>
//            <p>{retr.links}</p>
//            </div>
//          )

//      })
//      this.setState({data_val: data_val});
//      console.log("state",this.state.data_val);
//    })
 // // document.write(result.near_earth_objects[val][index])
 //          let display = result.near_earth_objects[val][index];
 //           // document.getElementById('root').innerHTML += (JSON && JSON.stringify ? JSON.stringify(display) : display) + '<br />';
 //          let display_obj_2_json = (JSON && JSON.stringify ? JSON.stringify(display) : display) ;
 //          document.getElementById('root').innerHTML += display_obj_2_json;
 //          // document.write(display_obj_2_json);
 //          console.log(display)
 //          // document.getElementById('root').innerHTML = console.log(result.near_earth_objects[val][index]);

 //          // document.write = result.near_earth_objects[val][index];
 //          const data_temp = result.near_earth_objects[val][index]