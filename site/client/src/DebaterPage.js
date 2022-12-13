import React from "react";
import RoundRow from "./RoundRow";
import Header from "./Header";
import "./DebaterPage.css";
import { API_BASE_URL } from "./utils";
import { IconButton, Tooltip } from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";

class DebaterPage extends React.Component {
  state = {
    rounds: [],
    debater: {},
    loading: 0,
    rankings: [],
    allDebaters: [],
    dataMissing: false,
  };

  getWinrate = () => {
    return `${(100 * this.state.debater.winrate).toFixed(1)}%`;
  };

  getRank = () => {
    const idx = this.state.rankings.findIndex(
      (debater) => debater.code === this.state.debater.code
    );
    if (idx === -1) {
      return (
        <>
          <span>Rank: N/A</span>
          <Tooltip
            title="Debaters are only ranked after participating in at least 10 rounds"
            style={{ marginBottom: "4px" }}
          >
            <IconButton>
              <InfoIcon />
            </IconButton>
          </Tooltip>
        </>
      );
    }
    return `Rank: ${idx + 1}`;
  };

  loaded = () => {
    this.setState({
      loading: this.state.loading + 1,
    });
  };

  hasAllInfo = () => {
    return this.state.debater.name !== "" && this.state.debater.school !== "";
  };

  componentDidMount() {
    const codeParam = new URLSearchParams(window.location.search).get("code");
    fetch(`${API_BASE_URL}/users/get_rounds?code=${codeParam}`)
      .then((res) => res.json())
      .then((rounds) => {
        rounds.reverse();
        this.setState({ rounds });
        this.loaded();
      });
    fetch(`${API_BASE_URL}/users/rankings`)
      .then((res) => res.json())
      .then((rankings) => {
        this.setState({ rankings });
        this.loaded();
      });
    fetch(`${API_BASE_URL}/users/all_debaters`)
      .then((res) => res.json())
      .then((allDebaters) => {
        this.setState({ allDebaters });
        this.loaded();
      });
    fetch(`${API_BASE_URL}/users/get_debater?code=${codeParam}`)
      .then((res) => res.json())
      .then((debater) => {
        this.setState({ debater });
        this.loaded();
        if (Object.keys(debater).length === 0) {
          this.setState({ dataMissing: true });
        }
      });
  }

  render() {
    if (this.state.loading < 4) return <div className="DebaterPage"></div>;
    return (
      <div className="DebaterPage">
        <Header debaterData={this.state.allDebaters} />
        {this.state.dataMissing ? (
          <h1>Unknown debater code</h1>
        ) : (
          <>
            <h1>{this.state.debater.name}</h1>
            <h3>{this.state.debater.code}</h3>
            <br />
            <div className="debater_info">
              {this.hasAllInfo() && <h4>{this.getRank()}</h4>}
              <h4>{`Elo: ${this.state.debater.elo}`}</h4>
              <h4>{`Winrate: ${this.getWinrate()}`}</h4>
              <h4>{`Rounds: ${this.state.debater.num_rounds}`}</h4>
            </div>
            <br />
            <br />
            <div className="rounds">
              {this.state.rounds.map((round, index) => (
                <>
                  <RoundRow
                    round={round}
                    debater={this.state.debater}
                    key={index}
                    rowIndex={index}
                    allDebaters={this.state.allDebaters}
                  />
                  {index + 1 < this.state.rounds.length &&
                  this.state.rounds[index + 1].tournament_id !=
                    round.tournament_id ? (
                    <>
                      <br /> <br />
                    </>
                  ) : null}
                </>
              ))}
            </div>
          </>
        )}
      </div>
    );
  }
}

export default DebaterPage;
