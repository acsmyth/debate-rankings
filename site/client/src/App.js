import React from "react";
import "./App.css";
import { createTheme, MuiThemeProvider } from "@material-ui/core/styles";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import RankingsPage from "./RankingsPage";
import DebaterPage from "./DebaterPage";

const theme = createTheme({
  // palette: {
  //   type: "dark",
  // },
  typography: {
    fontFamily: "Lato",
    fontSize: 12,
  },
  // overrides: {
  //   MuiTypography: {
  //     colorInherit: {
  //       color: "#fff",
  //     },
  //   },
  // },
});

class App extends React.Component {
  state = { rows: [] };

  render() {
    return (
      <Router>
        <MuiThemeProvider theme={theme}>
          <div className="App">
            <Switch>
              <Route
                exact
                path="/"
                render={(props) => <RankingsPage key={props.location.key} />}
              />
              <Route
                exact
                path="/debater"
                render={(props) => <DebaterPage key={props.location.key} />}
              />
            </Switch>
          </div>
        </MuiThemeProvider>
      </Router>
    );
  }
}

export default App;
