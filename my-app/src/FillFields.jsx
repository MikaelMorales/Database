import * as React from "react";
import TextField from 'material-ui/TextField';
import {Card, CardHeader} from "material-ui/Card";
import RaisedButton from "material-ui/RaisedButton";
import update from 'immutability-helper';
import axios from "axios";
import CircularProgress from 'material-ui/CircularProgress';
import Snackbar from 'material-ui/Snackbar';

class FillFields extends React.Component {
    constructor(props) {
        super(props);
        this.state = {requiredFieldValues: {}, optionalFieldValues: {}, waiting: false, toast: ""}
    }

    requiredFieldsOnChange = (event, field) => {
        let copyObject = update(this.state.requiredFieldValues, {
           [field]: {$set: event.target.value}
        });
        this.setState({requiredFieldValues: copyObject});
    }

    optionalFieldsOnChange = (event, field) => {
        let copyObject = update(this.state.optionalFieldValues, {
           [field]: {$set: event.target.value}
        });
        this.setState({optionalFieldValues: copyObject});
    }

    handleSubmit = (event) => {
        let valid = true;
        this.props.requiredFields.map((field) => {
            if (typeof this.state.requiredFieldValues[field] == "undefined" || this.state.requiredFieldValues[field] == "") {
                valid = false;
            }
        });
        if (valid) {
            this.sendRequest();
        } else {
            console.log("required fields not filled");
            // message to the user to tell him to fill the required fields.
        }
    }

    sendRequest = () => {
        axios.post(this.props.url, this.props.getBody(this.state.requiredFieldValues, this.state.optionalFieldValues))
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
                            label={this.props.submitLabel}
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
            let requiredFieldBlock;
            console.log(this.props.requiredFields)
            if (this.props.requiredFields.length) {
                requiredFieldBlock = (
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
                );
            }
            return (
                <div>

                    <div style={style.selectAndSubmit}>
                        {this.props.selectOp}
                        <RaisedButton
                            label={this.props.submitLabel}
                            primary={true}
                            style={style.submitButton}
                            onClick={this.handleSubmit}
                        />
                    </div>

                    <div style={style.itemsContainer}>

                        {requiredFieldBlock}

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

export default FillFields;
