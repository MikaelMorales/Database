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

    constructor(props) {
        super(props);
        this.state = {currentPageNb: 0};
    }

	render() {
    let rowId = 0;
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
                    tableLayout: 'auto',
                     overflowX: "auto",
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
				},
                cardStyle: {
                    minWidth: "60%"
                }
			}
			return (
				<div style={style.tableContainer}>
					<Card style={style.cardStyle}>
						<CardHeader
					      title={this.props.tableName}
					      style={style.cardHeaderStyle}
					    />
						<Table
							style={style.tableStyle}
							fixedHeader={true}
                            bodyStyle={{height: 'inherit', overflow: 'auto'}}
						>

						    <TableBody displayRowCheckbox={false} showRowHover={true} style={{marginTop: 0}}>
                                <TableRow>
						      		{this.props.columnNames.map((name) =>
						      			<TableRowColumn key={name} style={style.headerStyle}>{name}</TableRowColumn>
						      		)}
						     	 </TableRow>
						    	{this.props.items.map((item) =>
						    		<TableRow key={++rowId} >
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
