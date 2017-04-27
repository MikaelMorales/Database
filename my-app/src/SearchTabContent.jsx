import * as React from "react";
import SearchBar from "./SearchBar";
import Checkbox from 'material-ui/Checkbox';
import RaisedButton from "material-ui/RaisedButton";

class SearchTabContent extends React.Component {

	submitStateEnum = {
        "ABLE": 0,
        "DISABLE": 1
    };

	constructor(props) {
		super(props);
		this.state = {value: "", submitState: this.submitStateEnum.DISABLE, advancedOpt: false, selectedTables: new Set()}
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
		fetch('http://localhost/search_request.php', {
			method: 'POST',
			// headers: {
		 //    	'Accept': 'application/json',
		 //    	'Content-Type': 'application/json',
		 //    },
		    body: JSON.stringify({
		    	'Request': this.state.value,
		    	'Tables': Array.from(this.state.selectedTables).toString()
		    })
		})
		
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
	                handleSubmit={this.handleSubmit}
	                buttonLabel={"Search"}
	                buttonDisabled={this.state.submitState !== this.submitStateEnum.ABLE}/>

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