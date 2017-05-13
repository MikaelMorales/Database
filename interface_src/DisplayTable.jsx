import * as React from "react";
import {
  Table,
  TableBody,
  TableHeader,
  TableHeaderColumn,
  TableRow,
  TableRowColumn,
} from 'material-ui/Table';
import {Card, CardHeader} from 'material-ui/Card';

class DisplayTable extends React.Component {

	render() {
		console.log("items");
		console.log(this.props.items);
		if (!Object.keys(this.props.items).length) {
			return (<div/>);
		} else {
			const style = {
				tableContainer: {
					display: "flex",
					justifyContent: "center",
					marginTop: 20,
					marginBottom: 20
				},
				tableStyle: {
					maxWidth: "1000px",
					margin: 30,
				},
				superHeaderStyle: {
					fontWeight: "bold",
					textAlign: 'center'
				},
				headerStyle: {
					fontWeight: "bold"
				},
				cardHeaderStyle: {
					backgroundColor: "#EFEFEF"
				}
			}
			return (
				<div style={style.tableContainer}>
					<Card>
						<CardHeader
					      title={this.props.tableName}
					      style={style.cardHeaderStyle}
					    />
						<Table
							style={style.tableStyle}
							fixedHeader={true}
						>
						    <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
						      	<TableRow>
						      		{this.props.columnNames.map((name) =>
						      			<TableHeaderColumn key={name} style={style.headerStyle}>{name}</TableHeaderColumn>
						      		)}
						     	 </TableRow>
						    </TableHeader>
						    <TableBody displayRowCheckbox={false} showRowHover={true}>
						    	{this.props.items.map((item) =>
						    		<TableRow key={item["id"]} >
						    			{this.props.columnNames.map((name) =>
						    				<TableRowColumn key={name}>{item[name]}</TableRowColumn>
						    			)}
						    		</TableRow>
						    	)}
						    </TableBody>
						</Table>
					</Card>
				</div>
			);
		}
	}
}

export default DisplayTable;
