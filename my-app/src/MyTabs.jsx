import React, { Component } from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import injectTapEventPlugin from 'react-tap-event-plugin';
import SearchTabContent from "./SearchTabContent";


class MyTabs extends Component {

	constructor(props) {
		super(props);
		injectTapEventPlugin();
	}

	render() {
		return (
			<Tabs inkBarStyle={{background: '#EFEFEF'}} >
				<Tab label="Search">
					<SearchTabContent/>
			    </Tab>

				<Tab label="Predifined Queries">
					
			    </Tab>

			    <Tab label="Insert/Delete">

			    </Tab>

			</Tabs>
		)
	}
}

export default MyTabs;