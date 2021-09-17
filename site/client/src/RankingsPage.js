import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { Link } from "react-router-dom";
import Header from "./Header";
import "./RankingsPage.css";

class RankingsPage extends React.Component {
  state = {
    rows: [],
    isLoading: true,
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
    fetch("http://localhost:3001/users/rankings")
      .then((res) => res.json())
      .then((rows) => {
        this.setState({ rows, isLoading: false });
      });
  }

  render() {
    return (
      <div className="RankingsPage">
        <Header />
        <h1>2020-2021 Lincoln-Douglas Rankings</h1>
        <div style={{ height: "580px", width: "70%", margin: "auto" }}>
          {!this.state.isLoading && (
            <DataGrid
              rows={this.state.rows}
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
