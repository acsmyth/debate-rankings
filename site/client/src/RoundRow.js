import React from "react";
import { Link } from "react-router-dom";
import Header from "./Header";
import "./RoundRow.css";

class RoundRow extends React.Component {
  isDebaterA = () =>
    this.props.debater.code === this.props.round.debater_a_code;

  isBye = () => this.props.round.result === "Bye";

  getOpponent = () => {
    if (this.isBye()) return <a />;
    const maybeVs = this.isBye() ? "" : "vs ";
    if (this.isDebaterA()) {
      const code = this.props.round.debater_b_code
        .replaceAll("  ", " ")
        .replaceAll(" ", "_");
      return (
        <Link to={`/debater?code=${code}`}>
          {maybeVs + this.props.round.debater_b_code}
        </Link>
      );
    } else {
      console.log(this.props.round.debater_a_code);
      const code = this.props.round.debater_a_code
        .replaceAll("  ", " ")
        .replaceAll(" ", "_");
      return (
        <Link to={`/debater?code=${code}`}>
          {maybeVs + this.props.round.debater_a_code}
        </Link>
      );
    }
  };

  getResult = () => {
    if (this.isDebaterA()) {
      return this.sameResult(this.props.round.result);
    } else {
      return this.oppositeResult(this.props.round.result);
    }
  };

  sameResult = (result) => {
    if (result.includes("[")) {
      return result
        .replaceAll('"', "")
        .replaceAll("[", "")
        .replaceAll("]", "")
        .split(",")
        .join(", ");
    } else {
      return result;
    }
  };

  oppositeResult = (result) => {
    if (result.includes("[")) {
      return result
        .replaceAll('"', "")
        .replaceAll("[", "")
        .replaceAll("]", "")
        .split(", ")
        .map((res) => (res === "W" ? "L" : "W"))
        .join(", ");
    } else {
      return result === "W" ? "L" : "W";
    }
  };

  getDate = () => {
    const d = this.props.round.date.split("-");
    return `${d[1]}/${d[2]}/${d[0]}`;
  };

  getBackgroundColor = () =>
    this.props.rowIndex % 2 === 0 ? "rgb(211,211,211)" : "rgb(224,224,224)";

  render() {
    return (
      <div
        className="round_row"
        style={{ backgroundColor: this.getBackgroundColor() }}
      >
        <span className="result">{this.getResult()}</span>
        {this.getOpponent()}
        <span className="round_name">{this.props.round.round}</span>
        <span className="tournament_name">
          {this.props.round.tournament_name}
        </span>
        <span className="date">{this.getDate()}</span>
      </div>
    );
  }
}

export default RoundRow;
