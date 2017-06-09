import React, { Component } from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import injectTapEventPlugin from 'react-tap-event-plugin';
import SearchTabContent from "./SearchTabContent";
import QueryResultTabContent from "./QueryResultTabContent";
import PredifinedQueriesTabContent from "./PredifinedQueriesTabContent";
import InsertDeleteTabContent from "./InsertDeleteTabContent";
import axios from "axios";

class MyTabs extends Component {

	constructor(props) {
		super(props);
		this.state = {
			resultToDisplay: {},
			maxLineNb: 100,
			waiting: false,
			url: "",
			body: "",
			currentPage: 0,
			restOfRequest: false,
			tables: []
		};
		injectTapEventPlugin();
		this.getTables();
	}

	request = (url, body, nextPageDiff, restOfRequest) => { // restOfRequest allow us to know if we are requesting the rest of the current request or a new one.
		this.setState({waiting: true});
		let pageNb = this.state.currentPage + nextPageDiff;
		if (nextPageDiff === 0) {
			pageNb = 0;
		}
		body["Offset"] = pageNb * this.state.maxLineNb;
		body["MaxLineNb"] = this.state.maxLineNb;
		axios.post(url, body)
		.then((res) => {
			if (typeof res.data !== "undefined" && res.data !== null) {
				this.setState({resultToDisplay: res.data, waiting: false, url: url, body: body, currentPage: pageNb, restOfRequest: restOfRequest});
			}
		})
		.catch((res) => {
			this.setState({waiting: false});
		});
	}

	getTables = () => {
		axios.post('http://localhost/get_tables.php')
		.then((res) => {
			console.log("OK");
			console.log(res.data);
			if (typeof res.data !== "undefined" && res.data !== null) {
				this.setState({tables: res.data});
			}
		})
		.catch((res) => {
			console.log(res);
		})
	}

	render() {
		return (
			<Tabs inkBarStyle={{background: '#EFEFEF'}} >
				<Tab label="Search">
					<SearchTabContent
						request={this.request}
						waiting={this.state.waiting}
						tables={this.state.tables}
					/>
			    </Tab>

				<Tab label="Predifined Queries">
						<PredifinedQueriesTabContent
							request={this.request}
							waiting={this.state.waiting}
						/>
			  </Tab>

			    <Tab label="Query Results">
			    	<QueryResultTabContent
				    	resultToDisplay={this.state.resultToDisplay}
						url={this.state.url}
						body={this.state.body}
						request={this.request}
						currentPage={this.state.currentPage}
						prevDisabled={this.state.currentPage === 0}
						restOfRequest={this.state.restOfRequest}
						waiting={this.state.waiting}
			    	/>
			    </Tab>

			    <Tab label="Insert/Delete">

					<InsertDeleteTabContent
						tables={this.state.tables}
					/>

			    </Tab>

			</Tabs>
		)
	}
}

export default MyTabs;
