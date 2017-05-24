import * as React from "react";
import DropDownMenu from 'material-ui/DropDownMenu';
import MenuItem from 'material-ui/MenuItem';
import axios from "axios";
import Paper from 'material-ui/Paper';
import CircularProgress from 'material-ui/CircularProgress';
import FillFields from "./FillFields";

class InsertDeleteTabContent extends React.Component {

    constructor(props) {
        super(props);
        this.state = {opType: 1, table: 0, tableInfo: {}, waiting: false};
    }

    getTableInfos = () => {
		axios.post('http://localhost/get_table_infos.php', {
            tableId: this.state.table
        })
	    .then((res) => {
			this.setState({waiting: false, tableInfo: res['data']});
		})
		.catch((res) => {
			this.setState({waiting: false});
		});
    }

    onSelectTable = (e, index, value) => {
        if (value !== 0) {
            this.setState({waiting: true, table: value}, () => this.getTableInfos());
        } else {
            this.setState({table: value});
        }
    }

    getBodyInsert = (requiredFieldValues, optionalFieldValues) => {
        let attributes = Object.assign({}, requiredFieldValues, optionalFieldValues);
        const filtered = Object.keys(attributes).reduce((filtered, key) => {
            if (attributes[key] !== "undefined" && attributes[key] !== "") {
                filtered[key] = attributes[key];
            }
            return filtered;
        }, {});
        return {
            Table: this.state.table,
            Attributes: filtered
        };
    }

    getBodyDelete = (requiredFieldValues, optionalFieldValues) => {
        const attributes = Object.keys(optionalFieldValues).reduce((filtered, key) => {
            if (optionalFieldValues[key] !== "undefined" && optionalFieldValues[key] !== "") {
                filtered[key] = optionalFieldValues[key];
            }
            return filtered;
        }, {});

        return {
            Table: this.state.table,
            Attributes: attributes
        };
    }

    render() {
        const style = {
            dropDownStyle: {
                width: 200,
            },
            paper: {
                maxWidth: 450,
                margin: "auto",
                marginTop: 30,
                paddingBottom: 10
            },
            progress: {
                marginTop: "50px"
            },
            waiting: {
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
            }
        };

        const selectOp =
            <div>
                <Paper style={style.paper}>
                    <DropDownMenu value={this.state.opType} onChange={(e, index, newOpType) => this.setState({opType: newOpType})} style={style.dropDownStyle}>
                        <MenuItem value={1} primaryText="Insert"/>
                        <MenuItem value={2} primaryText="Delete"/>
                     </DropDownMenu>

                     <DropDownMenu value={this.state.table} onChange={this.onSelectTable} style={style.dropDownStyle}>
                         <MenuItem value={0} primaryText="Choose a table" />
                         {this.props.tables.map((table) =>
                             <MenuItem key={table["id"]} value={table["id"]} primaryText={table["name"]}/>
                         )}

                     </DropDownMenu>
                 </Paper>
            </div>;

        if (this.state.opType === 1) {
            if (!this.state.waiting && this.state.table !== 0) {
                const requiredFields = this.state.tableInfo[this.state.table].filter((item) => item["Null"] === "NO").map(item => item["Field"]);
                const notRequiredFields = this.state.tableInfo[this.state.table].filter((item) => item["Null"] !== "NO").map(item => item["Field"]);
                // return (
                //     <div>
                //         <InsertEntity
                //             selectOp={selectOp}
                //             requiredFields={requiredFields}
                //             notRequiredFields={notRequiredFields}
                //             table={this.state.table}
                //         />
                //     </div>
                // );
                return (
                    <div>
                        <FillFields
                            selectOp={selectOp}
                            requiredFields={requiredFields}
                            notRequiredFields={notRequiredFields}
                            table={this.state.table}
                            submitLabel={"Add"}
                            url="http://localhost/insert_in_db.php"
                            getBody={this.getBodyInsert}
                        />
                    </div>
                );
            } else if (this.state.waiting) {
                return (
                    <div style={{display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center"}}>
                        {selectOp}

                        <CircularProgress size={100} thickness={10} color="#E24E42" style={style.progress}/>
                    </div>
                );
            } else {
                return (
                    <div>
                        {selectOp}

                    </div>
                );
            }
        } else {
            if (!this.state.waiting && this.state.table !== 0) {
                const fields = this.state.tableInfo[this.state.table].map(item => item["Field"]);
                // return (
                //     <div>
                //         <DeleteEntity
                //             selectOp={selectOp}
                //             fields={fields}
                //             table={this.state.table}
                //         />
                //     </div>
                // );

                return (
                    <div>
                        <FillFields
                            selectOp={selectOp}
                            requiredFields={[]}
                            notRequiredFields={this.state.tableInfo[this.state.table].map(item => item["Field"])}
                            table={this.state.table}
                            submitLabel={"Delete"}
                            url="http://localhost/delete_from_db.php"
                            getBody={this.getBodyDelete}
                        />
                    </div>
                );
            } else {
                return (
                    <div>
                        {selectOp}

                    </div>
                );
            }
        }
    }
}

export default InsertDeleteTabContent;
