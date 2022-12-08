import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { Link } from "react-router-dom";
import Header from "./Header";
import "./RankingsPage.css";
import { API_BASE_URL } from "./utils";

class RankingsPage extends React.Component {
  state = {
    rankings: [],
    allDebaters: [],
    loading: 0,
  };

  renderBold = (params) => <b>{params.colDef.headerName}</b>;

  columns = [
    {
      headerName: "Rank",
      field: "id",
      flex: 0.7,
      renderHeader: this.renderBold,
    },
    {
      headerName: "Code",
      field: "code",
      flex: 1.7,
      renderHeader: this.renderBold,
      renderCell: (params) => (
        <Link to={`/debater?code=${params.value.replaceAll(" ", "_")}`}>
          {params.value}
        </Link>
      ),
    },
    {
      headerName: "Name",
      field: "name",
      flex: 1.1,
      renderHeader: this.renderBold,
    },
    {
      headerName: "School",
      field: "school",
      flex: 0.9,
      renderHeader: this.renderBold,
    },
    {
      headerName: "Elo",
      field: "elo",
      flex: 0.75,
      renderHeader: this.renderBold,
    },
    {
      headerName: "Win %",
      field: "winrate",
      flex: 0.9,
      renderHeader: this.renderBold,
      valueFormatter: (params) => {
        const valueFormatted = (params.value * 100).toFixed(1);
        return `${valueFormatted}%`;
      },
    },
    {
      headerName: "# Rounds",
      field: "num_rounds",
      flex: 0.9,
      renderHeader: this.renderBold,
    },
  ];

  componentDidMount() {
    fetch(`${API_BASE_URL}/users/rankings`)
      .then((res) => res.json())
      .then((rankings) => {
        this.setState({ rankings, loading: this.state.loading + 1 });
      });
    fetch(`${API_BASE_URL}/users/all_debaters`)
      .then((res) => res.json())
      .then((allDebaters) => {
        this.setState({ allDebaters, loading: this.state.loading + 1 });
      });
  }

  render() {
    return (
      <div className="RankingsPage">
        <Header debaterData={this.state.allDebaters} />
        <h1>2022-2023 Lincoln-Douglas Debate Elo Rankings</h1>
        <div style={{ height: "78vh", width: "70%", margin: "auto" }}>
          {this.state.loading === 2 && (
            <DataGrid
              rows={this.state.rankings.slice(0, 250)}
              columns={this.columns}
              rowsPerPageOptions={[]}
            />
          )}
        </div>
      </div>
    );
  }
}

export default RankingsPage;
