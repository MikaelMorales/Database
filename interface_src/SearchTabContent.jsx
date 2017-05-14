import * as React from "react";
import SearchBar from "./SearchBar";
import Checkbox from 'material-ui/Checkbox';
import RaisedButton from "material-ui/RaisedButton";
import CircularProgress from 'material-ui/CircularProgress';
import axios from "axios";
import DropDownMenu from 'material-ui/DropDownMenu';
import MenuItem from 'material-ui/MenuItem';

class SearchTabContent extends React.Component {

	constructor(props) {
		super(props);
		this.state = {value: "", advancedOpt: false, selectedTables: new Set(), waiting: false, requestType: 1}
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
		this.setState({waiting: true});
		let body;
		let url;
		if (this.state.requestType === 1) {
			body = {Request: this.state.value,
					Tables: Array.from(this.state.selectedTables).toString()
					};
			url = 'http://localhost/search_request.php';
		} else {
			body = {Statement: this.state.value};
			url = 'http://localhost/execute_sql_statement.php';
		}
		axios.post(url, body)
	    .then((res) => {
			this.props.pushResults(res.data);
			console.log(JSON.stringify(res.data));
			console.log(res.data["Story"]);
			this.setState({waiting: false});
		})
		.catch((res) => {
			console.log(res);
			this.setState({waiting: false});
		});
	}

	handleCheckboxCheck = (value, checked) => {
		if (checked) {
			this.state.selectedTables.add(value)
		} else {
			this.state.selectedTables.delete(value)
		}
		// this.setState({selectedTables: this.state.selectedTables})
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
		if (this.state.waiting) {
			circular = <CircularProgress size={100} thickness={10} color="#E24E42" style={style.wait} />;
		}

		let advOpt = null;
		if (this.state.advancedOpt) {
			advOpt = (
				<div>
					<h3 style={{fontWeight: "normal"}}>Tables to search:</h3>
					<Checkbox
						label="Story"
						onCheck={(e, checked) => this.handleCheckboxCheck("Story", checked)}
					/>
					<Checkbox
						label="Artists"
						onCheck={(e, checked) => this.handleCheckboxCheck("Story_Artists", checked)}
					/>
					<Checkbox
						label="Characters"
						onCheck={(e, checked) => this.handleCheckboxCheck("Story_Characters", checked)}
					/>
				</div>
			)
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
		                buttonDisabled={this.state.waiting}/>

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
        	</div>
        );
	}
}

export default SearchTabContent;
