import * as React from "react";
import {List, ListItem} from 'material-ui/List';
import RaisedButton from "material-ui/RaisedButton";
import {Card} from 'material-ui/Card';
import axios from "axios";
import CircularProgress from 'material-ui/CircularProgress';
import Snackbar from 'material-ui/Snackbar';

class PredifinedQueriesTabContent extends React.Component {

  constructor(props) {
    super(props);
    this.state = {toast: ""};
  }

  idToTitle = [
    {id: 0, title: "Print the brand group names with the highest number of Belgian indicia publishers."},
    {id: 1, title: "Print the ids and names of publishers of Danish book series."},
    {id: 2, title: "Print the names of all Swiss series that have been published in magazines."},
    {id: 3, title: "Starting from 1990, print the number of issues published each year."},
    {id: 4, title: "Print the number of series for each indicia publisher whose name resembles \'DC comics\'."},
    {id: 5, title: "Print the titles of the 10 most reprinted stories."},
    {id: 6, title: "Print the artists that have scripted, drawn, and colored at least one of the stories they were involved in."},
    {id: 7, title: "Print all non-reprinted stories involving Batman as a non-featured character."},
  ];

  executePredifinedQuery = (id) => {
      let url = "http://localhost/fetch_predifined_queries.php";
      let body = {
          QueryId: id
      };
      this.props.request(url, body, 0, false);



    // this.setState({waiting: true});
    // event.preventDefault();
	// 	axios.post('http://localhost/fetch_predifined_queries.php', {
	// 	    QueryId: id
	//     })
	//     .then((res) => {
	// 		console.log(res.data);
    //   this.props.pushResults(res.data);
    //   this.setState({waiting: false});
	// 	})
	// 	.catch((res) => {
	// 		console.log(res);
    //         this.setState({waiting: false, toast: res["data"]});
	// 	});
	}

  render() {
    const style = {
      container: {
        maxWidth: 1000,
        margin: "auto"
      },
      item: {
        margin: 10,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      },
      executeButton: {
        minWidth: 200
      },
      card: {
        maxWidth: 1000,
        margin: "auto"
      },
      wait: {
        maxWidth: 200,
        margin: "auto",
        padding: 20
      }
    }

    let circular;
    if (this.props.waiting) {
      circular = <CircularProgress size={100} thickness={10} color="#E24E42" />;
    }
    return (
    <div style={style.container}>
      <div style={style.wait}>
        {circular}
      </div>
      <Card style={style.card}>
          <List>
            {this.idToTitle.map((item) =>
              <div key={item.id} style={style.item}>
                <ListItem
                    primaryText={item.title}
                    onClick={(e) => this.executePredifinedQuery(item.id)}
                    disabled={this.props.waiting}
                />
              </div>
            )}
          </List>
      </Card>

      <Snackbar
       open={this.state.toast !== null && this.state.toast !== ""}
       message={this.state.toast}
       autoHideDuration={4000}
       onRequestClose={(e) => this.setState({toast: ""})}
     />
    </div>
    );
  }
}

export default PredifinedQueriesTabContent;
