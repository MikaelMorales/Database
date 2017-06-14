import * as React from "react";
import SearchBar from "./SearchBar";
import Checkbox from 'material-ui/Checkbox';
import RaisedButton from "material-ui/RaisedButton";
import CircularProgress from 'material-ui/CircularProgress';
import DropDownMenu from 'material-ui/DropDownMenu';
import MenuItem from 'material-ui/MenuItem';
import Snackbar from 'material-ui/Snackbar';

class SearchTabContent extends React.Component {

	constructor(props) {
		super(props);
		this.state = {value: "", advancedOpt: false, selectedTables: new Set(), requestType: 1, toast: ""}
	}

	handleChange = (event) => {
        let submitState = 1;
        if(event.target.value !== "") {
            submitState = 0;
        }
        this.setState({value: event.target.value, submitState: submitState});
    }

    handleSubmit = (event) => {
		event.preventDefault();

		let body;
		let url;
		if (this.state.requestType === 1) {
			body = {Request: this.state.value,
					Tables: Array.from(this.state.selectedTables).toString(),
					};
			url = 'http://localhost/search_request.php';
		} else {
			body = {
				Statement: this.state.value,
			};
			url = 'http://localhost/execute_sql_statement.php';
		}

		this.props.request(url, body, 0, false);
	}

	handleCheckboxCheck = (value, checked) => {
		if (checked) {
			this.state.selectedTables.add(value)
		} else {
			this.state.selectedTables.delete(value)
		}
	}

	render() {
		const style = {
			advOptButtonStyle: {
				display: "flex",
				flexDirection: "column",
				alignItems: "center",
				minWidth: "1000px"
			},
			wait: {
				marginTop: 50
			},
			searchContainer: {
				display: "flex",
				flexDirection: "line",
				alignItems: "center",
				marginTop: "200px",
				justifyContent: "spaceAround"
			},
			dropDownStyle: {
				minWidth: 200
			}
		}

		let circular;
		if (this.props.waiting) {
			circular = <CircularProgress size={60} thickness={10} color="#E24E42" style={style.wait} />;
		}

		let advOpt = null;
		if (this.state.advancedOpt && this.props.tables.length > 0) {
			advOpt = (
				<div>
					<h3 style={{fontWeight: "normal"}}>Tables to search:</h3>
					{this.props.tables.map((table) =>
						<Checkbox
							key={table["id"]}
							label={table["name"]}
							onCheck={(e, checked) => this.handleCheckboxCheck(table["id"], checked)}
						/>
					)}
				</div>
			);
		}

		return (
			<div style={style.advOptButtonStyle}>

				{circular}

				<div style={style.searchContainer}>
					<SearchBar
		                hint={this.state.requestType === 1 ? "Type here to search..." : "Enter a SQL query..."}
		                value={this.state.value}
		                handleChange={this.handleChange}
		                handleSubmit={(e) => this.handleSubmit(e)}
		                buttonLabel={"Search"}
		                buttonDisabled={this.props.waiting}/>

					<DropDownMenu value={this.state.requestType} onChange={(e, index, value) => this.setState({requestType: value})} style={style.dropDownStyle}>
					 <MenuItem value={1} primaryText="Keyword" />
					 <MenuItem value={2} primaryText="SQL statement" />
				   </DropDownMenu>

			   </div>

	            <RaisedButton
	            	label={"Advanced Options"}
	                type="submit"
	                onClick={() => this.setState({advancedOpt: !this.state.advancedOpt})}
	                style={{marginTop: "50px"}}
	            />


            	{advOpt}

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

export default SearchTabContent;
