import * as React from "react";
import TextField from 'material-ui/TextField';
import {Card, CardHeader} from "material-ui/Card";
import RaisedButton from "material-ui/RaisedButton";
import update from 'immutability-helper';
import axios from "axios";
import CircularProgress from 'material-ui/CircularProgress';
import Snackbar from 'material-ui/Snackbar';

class InsertEntity extends React.Component {
    constructor(props) {
        super(props);
        this.state = {requiredFieldsValues: {}, optionalFieldsValues: {}, waiting: false, toast: ""}
    }

    requiredFieldsOnChange = (event, field) => {
        let copyObject = update(this.state.requiredFieldsValues, {
           [field]: {$set: event.target.value}
        });
        this.setState({requiredFieldsValues: copyObject});
    }

    optionalFieldsOnChange = (event, field) => {
        let copyObject = update(this.state.optionalFieldsValues, {
           [field]: {$set: event.target.value}
        });
        this.setState({optionalFieldsValues: copyObject});
    }

    handleSubmit = (event) => {
        let valid = true;
        this.props.requiredFields.map((field) => {
            if (typeof this.state.requiredFieldsValues[field] == "undefined" || this.state.requiredFieldsValues[field] == "") {
                valid = false;
            }
        });
        if (valid) {
            this.sendRequest();
        } else {
            // message to the user to tell him to fill the required fields.
        }
    }

    sendRequest = () => {
        const attributes = Object.assign({}, this.state.requiredFieldsValues, this.state.optionalFieldsValues);
        console.log(attributes);
        axios.post('http://localhost/insert_in_db.php', {
            Table: this.props.table,
            Attributes: attributes
        })
	    .then((res) => {
			console.log(res);
            this.setState({waiting: false, toast: res["data"]});
		})
		.catch((res) => {
			console.log(res);
			this.setState({waiting: false, toast: res["data"]});
		});
    }

    render() {
        const style = {
            globalContainer: {
                display: "flex",
                justifyContent: "center",
            },
            itemsContainer: {
                display: "flex",
                flexWrap: "wrap",
                justifyContent: "center",
                alignItems: "center"
            },
            card: {
                display: "flex",
                flexWrap: "wrap",
                margin: "30px",
                maxWidth: "80%"
            },
            cardHeader: {
                backgroundColor: "#EFEFEF",
            },
            textField: {
                margin: "30px"
            },
            selectAndSubmit: {
                display: "flex",
                justifyContent: "center",
                alignItems: "center"
            },
            submitButton: {
                marginTop: 30,
                marginLeft: 50
            }
        }

        if (this.state.waiting) {
            return (
                <div>
                    <div style={style.selectAndSubmit}>
                        {this.props.selectOp}
                        <RaisedButton
                            label={"Add"}
                            primary={true}
                            style={style.submitButton}
                            onClick={this.handleSubmit}
                            disabled={true}
                        />
                    </div>

                    <div style={style.itemsContainer}>
                        <CircularProgress />
                    </div>

                </div>
            )

        } else {
            return (
                <div>

                    <div style={style.selectAndSubmit}>
                        {this.props.selectOp}
                        <RaisedButton
                            label={"Add"}
                            primary={true}
                            style={style.submitButton}
                            onClick={this.handleSubmit}
                        />
                    </div>

                    <div style={style.itemsContainer}>

                        <Card  style={style.card}>
                            <CardHeader
                                style={style.cardHeader}
                                title="Required fields"
                            />
                            {this.props.requiredFields.map((field) =>
                                    <TextField
                                        key={field}
                                        style={style.textField}
                                        hintText={"Type the " + field}
                                        errorText="This field is required"
                                        floatingLabelText={field}
                                        onChange={(event) => this.requiredFieldsOnChange(event, field)}
                                    />
                            )}
                        </Card>

                        <Card  style={style.card}>
                            <CardHeader
                                style={style.cardHeader}
                                title="Optional fields"
                            />
                            {this.props.notRequiredFields.map((field) =>
                                    <TextField
                                        key={field}
                                        style={style.textField}
                                        hintText={"Type the " + field}
                                        floatingLabelText={field}
                                        onChange={(event) => this.optionalFieldsOnChange(event, field)}
                                    />
                            )}
                        </Card>
                    </div>

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
}

export default InsertEntity;
