import React, { Component } from 'react';
const fs = require("fs")
export default class Api_retrieval extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: []
    };
  }

  componentDidMount() {
    fetch("https://api.nasa.gov/neo/rest/v1/feed?start_date=2019-09-06&end_date=2019-09-07&&id=2465617&results=1&api_key=KwRDL3x7w75naVBiJua5GmSpMEDn75yNMjMqacS8")
      .then(res => res.json())
      .then(
        (result) => {
          // const first_numeric_key = 2019-09-06;
          // first_numeric_key = first_numeric_key.toString();
          const val = "2019-09-06";
          const index = "0";
          document.write(result.near_earth_objects[val][index])
          console.log(result.near_earth_objects[val][index])
          // document.getElementById('root').innerHTML = console.log(result.near_earth_objects[val][index]);

          document.write = result.near_earth_objects[val][index];
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
    const { error, isLoaded, items } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <p>Its fetching</p>
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