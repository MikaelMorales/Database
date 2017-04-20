import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MyTabs from "./MyTabs";


class App extends Component {

  muiTheme = getMuiTheme({
    tabs: {
        backgroundColor: "#BFBFBF"
    },
    raisedButton: {
      primaryColor: "#E24E42",
    },
    checkbox: {
      checkedColor: "#E24E42",

    }
  })

  render() {
    return (
      <MuiThemeProvider muiTheme={this.muiTheme}>
        <div className="App">
          <div className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
          <h2 className="App-title">The Comics Database</h2>
          </div>
          <MyTabs/>
        </div>
        </MuiThemeProvider>
    );
  }
}

export default App;
