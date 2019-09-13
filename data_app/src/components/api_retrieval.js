import React, { Component } from 'react';

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
    fetch("https://randomuser.me/api?results=500")
      .then(res => res.json())
      .then(
        (result) => {
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
// 			let data_val = data.results.map((retr) => {
// 				return(
// 						<div key={retr.results}>
// 						<p>{retr.links}</p>
// 						</div>
// 					)

// 			})
// 			this.setState({data_val: data_val});
// 			console.log("state",this.state.data_val);
// 		})