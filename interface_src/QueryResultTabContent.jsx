import * as React from "react";
import DisplayTable from "./DisplayTable";
import Divider from 'material-ui/Divider';


class QueryResultTabContent extends React.Component {
	render() {
		if (!Object.keys(this.props.resultToDisplay).length) {
			return (<h1>You have no query results</h1>);
		} else {
			const style = {
				containerStyle: {
				 	display: "flex",
				 	flexDirection: "column",
				 	justifyContent: "spaceBetween"
				}
			}
			return(
				<div>
					<DisplayTable
						tableName="Stories"
						columnNames={["id", "title"]}
						items={this.props.resultToDisplay["Story"]}
					/>

					<DisplayTable
						tableName="Artists"
						columnNames={["id", "name"]}
						items={this.props.resultToDisplay["Story_Artists"]}
					/>

					<DisplayTable
						tableName="Characters"
						columnNames={["id", "name"]}
						items={this.props.resultToDisplay["Story_Artists"]}
					/>

				</div>
			);
		}	
	}
}

export default QueryResultTabContent;