import * as React from "react";
import DisplayTable from "./DisplayTable";
import RightArrow from "material-ui/svg-icons/hardware/keyboard-arrow-right";
import LeftArrow from "material-ui/svg-icons/hardware/keyboard-arrow-left";
import IconButton from 'material-ui/IconButton';
import CircularProgress from 'material-ui/CircularProgress';

class QueryResultTabContent extends React.Component {

	toNextPage = (nextPage) => {
		this.props.request(this.props.url, this.props.body, nextPage, true);
	}

	render() {
		if (!Object.keys(this.props.resultToDisplay).length && !this.props.restOfRequest) {
			return (<h1 style={{maxWidth: 400, margin: "auto"}}>You have no query results</h1>);
		} else {
			const style = {
				containerStyle: {
				 	display: "flex",
				 	flexDirection: "column",
				 	justifyContent: "spaceBetween"
				},
				arrowContainer: {
					display: "flex",
					justifyContent: "center"
				},
				noPageStyle: {
					maxWidth: 400,
					margin: "auto"
				}
			}

			let noPage;
			if (this.props.resultToDisplay.length === 0) {
				noPage = <h1 style={style.noPageStyle}>No page anymore</h1>;
			}

			let circular;
			if (this.props.waiting) {
			  circular = <CircularProgress size={100} thickness={10} color="#E24E42" />;
			}
			return(
				<div style={style.containerStyle}>
					<div/>

				{noPage}

					{Object.keys(this.props.resultToDisplay).map((key) =>
						<DisplayTable
							key={key}
							tableName={key}
							columnNames={Object.keys(this.props.resultToDisplay[key][0])}
							items={this.props.resultToDisplay[key]}
						/>
					)}

					<div style={style.arrowContainer}>
						<IconButton
							tooltip="previous page"
							touch={true}
							tooltipPosition="top-left"
							onTouchTap={(e) => this.toNextPage(-1)}
							disabled={this.props.prevDisabled || this.props.waiting}
						>
							<LeftArrow />
						</IconButton>

						<IconButton
							tooltip="next page"
							touch={true}
							tooltipPosition="top-right"
							onTouchTap={(e) => this.toNextPage(1)}
							disabled={this.props.waiting || this.props.resultToDisplay.length === 0}
						>
							<RightArrow />
						</IconButton>
					</div>
					<div style={{display: "flex", justifyContent: "center"}}>
						{circular}
					</div>
				</div>

			);
		}
	}
}

export default QueryResultTabContent;
