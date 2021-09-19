import React from "react";
import RoundRow from "./RoundRow";
import Header from "./Header";
import "./DebaterPage.css";

class DebaterPage extends React.Component {
  state = {
    rounds: [],
    debater: {},
    loading: 0,
    rankings: [],
  };

  getWinrate = () => {
    return `${(100*this.state.debater.winrate).toFixed(1)}%`;
  }

  getRank = () => {
    const idx = this.state.rankings.findIndex(debater => debater.code == this.state.debater.code)
    if (idx === -1) {
      return 'N/A'
    }
    return idx+1;
  }

  loaded = () => {
    this.setState({
      loading: this.state.loading + 1
    })
  }

  hasAllInfo = () => {
    return this.state.debater.name !== '' && this.state.debater.school !== '';
  }
  
  componentDidMount() {
    const codeParam = new URLSearchParams(window.location.search).get("code");
    fetch(`https://www.debate-rankings.com/api/users/get_rounds?code=${codeParam}`)
      .then((res) => res.json())
      .then((rounds) => {
        rounds.reverse();
        this.setState({ rounds, loading: this.state.loading + 1 });
        this.loaded();
      });
    fetch(`https://www.debate-rankings.com/api/users/rankings`)
      .then((res) => res.json())
      .then((rankings) => {
        this.setState({ rankings });
        this.loaded();
      });
    fetch(`https://www.debate-rankings.com/api/users/get_debater?code=${codeParam}`)
      .then((res) => res.json())
      .then((debater) => {
        this.setState({ debater });
        this.loaded();
      }
    )
  }

  render() {
    if (this.state.loading < 3) return <div className="DebaterPage"></div>;
    console.log(this.state.debater);
    return (
      <div className="DebaterPage">
        <Header/>
        <h1>{this.state.debater.name}</h1>
        <h3>{this.hasAllInfo() ? this.state.debater.code + ", " + this.state.debater.school : this.state.debater.code}</h3>
        <br/>
        <div className="debater_info">
          {this.hasAllInfo() && <h4>{`Rank ${this.getRank()}`}</h4>}
          <h4>{`Elo: ${this.state.debater.elo}`}</h4>
          <h4>{`Winrate: ${this.getWinrate()}`}</h4>
        </div>
        <br/>
        <br/>
        <div className="rounds">
          {this.state.rounds.map((round, index) => (
            <RoundRow round={round} debater={this.state.debater} key={index} rowIndex={index}/>
          ))}
        </div>
      </div>
    );
  }
}

export default DebaterPage;
