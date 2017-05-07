import * as React from "react";
import SearchBar from "./SearchBar";
import Checkbox from 'material-ui/Checkbox';
import RaisedButton from "material-ui/RaisedButton";
import axios from "axios";

class SearchTabContent extends React.Component {

	constructor(props) {
		super(props);
		this.state = {value: "", advancedOpt: false, selectedTables: new Set(), disabled: false}
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
		this.setState({disabled: true});
		axios.post('http://localhost/search_request.php', {
		    Request: this.state.value,
	    	Tables: Array.from(this.state.selectedTables).toString()
	    })
	    .then((res) => {
			this.props.pushResults(res.data);
			console.log(JSON.stringify(res.data));
			console.log(res.data["Story"]);
			this.setState({disabled: false});
		})
		.catch((res) => {
			console.log(res);
			this.setState({disabled: false});
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
			}
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
				<SearchBar
	                hint={"Type here to search..."}
	                value={this.state.value}
	                handleChange={this.handleChange}
	                handleSubmit={(e) => this.handleSubmit(e)}
	                buttonLabel={"Search"}
	                buttonDisabled={this.state.disabled}/>

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