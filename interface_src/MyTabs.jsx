import React, { Component } from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import injectTapEventPlugin from 'react-tap-event-plugin';
import SearchTabContent from "./SearchTabContent";
import QueryResultTabContent from "./QueryResultTabContent";


class MyTabs extends Component {

	constructor(props) {
		super(props);
		this.state = {resultToDisplay: []}
		injectTapEventPlugin();
	}

	getResponse = (response) => {
		this.setState({resultToDisplay: response});

	}

	render() {
		return (
			<Tabs inkBarStyle={{background: '#EFEFEF'}} >
				<Tab label="Search">
					<SearchTabContent 
						getResponse={this.getResponse}
					/>
			    </Tab>

				<Tab label="Predifined Queries">
					
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