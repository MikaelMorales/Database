import React, { Component } from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import injectTapEventPlugin from 'react-tap-event-plugin';
import SearchTabContent from "./SearchTabContent";
import QueryResultTabContent from "./QueryResultTabContent";
import PredifinedQueriesTabContent from "./PredifinedQueriesTabContent";

class MyTabs extends Component {

	constructor(props) {
		super(props);
		this.state = {resultToDisplay: {}}
		injectTapEventPlugin();
	}

	pushResults = (data) => this.setState({resultToDisplay: data});

	render() {
		return (
			<Tabs inkBarStyle={{background: '#EFEFEF'}} >
				<Tab label="Search">
					<SearchTabContent
						pushResults={this.pushResults}
					/>
			    </Tab>
					
				<Tab label="Predifined Queries">
						<PredifinedQueriesTabContent
								pushResults={this.pushResults}
						/>
			  </Tab>

			    <Tab label="Query Results">
			    	<QueryResultTabContent
				    	resultToDisplay={this.state.resultToDisplay}
			    	/>
			    </Tab>

			    <Tab label="Insert/Delete">

			    </Tab>

			</Tabs>
		)
	}
}

export default MyTabs;
