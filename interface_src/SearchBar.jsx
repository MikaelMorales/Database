import * as React from "react";
import TextField from "material-ui/TextField";
import Paper from "material-ui/Paper";
import { Menu, MenuItem } from "material-ui/Menu";
import RaisedButton from "material-ui/RaisedButton";


export default ({hint, value, handleChange, handleSubmit, buttonLabel, buttonDisabled}) => {

    
    const style = {
        formStyle: {
            display: "flex",
            justifyContent: "space-around",
            alignItems: "center",
            marginTop: "100px",
            minWidth: "1000px"
        },
        textFieldStyle: {
            flex: "0 0 auto",
            width: "95%"
        },
        paperStyle: {
            width: "80%"
        }
    }

    return (
        <form style={style.formStyle}>
            <Paper style={style.paperStyle}>
                <Menu disableAutoFocus={true}>
                    <MenuItem disabled={true}>
                        <TextField
                            hintText={hint}
                            underlineShow={false}
                            value={value}
                            onChange={handleChange}
                            style={style.textFieldStyle}
                        />
                    </MenuItem>
                </Menu>
            </Paper>

            <RaisedButton
                    label={buttonLabel}
                    type="submit"
                    primary={true}
                    onClick={handleSubmit}
                    disabled={buttonDisabled}
            />

            </form>
    );
};