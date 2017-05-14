import * as React from "react";
import DisplayTable from "./DisplayTable";

class QueryResultTabContent extends React.Component {

	tableToName = {"Story_Artists": "Artists", "Story_Characters": "Characters", "Brand_Group": "Brand Group"};

	getTableName(key) {
		if (key in this.tableToName) {
			return this.tableToName[key];
		} else {
			return key;
		}
	}

	render() {
		console.log("call to render method of query result tab content");
		if (!Object.keys(this.props.resultToDisplay).length) {
			console.log("result to display null or empty : ");
			console.log(JSON.stringify(this.props.resultToDisplay));
			return (<h1>You have no query results</h1>);
		} else {
			console.log("result to display ok : " + this.props.resultToDisplay);
			const style = {
				containerStyle: {
				 	display: "flex",
				 	flexDirection: "column",
				 	justifyContent: "spaceBetween"
				}
			}
			console.log(this.props.resultToDisplay);
			return(
				<div style={style.containerStyle}>
					<div/>

					{Object.keys(this.props.resultToDisplay).map((key) =>
						<DisplayTable
							key={key}
							tableName={this.getTableName(key)}
							columnNames={Object.keys(this.props.resultToDisplay[key][0])}
							items={this.props.resultToDisplay[key]}
						/>
					)}
				</div>

			);
		}
	}
}

export default QueryResultTabContent;
