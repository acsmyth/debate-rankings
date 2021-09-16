import React from "react";
import Logo from "./Logo";
import "./Header.css";

class Header extends React.Component {
  render() {
    return (
      <div className="header">
        <Logo />
        <a href="https://github.com/ACSmyth/debate-gg" target="_blank">
          <img src="github_logo.svg" width="30" />
        </a>
      </div>
    );
  }
}

export default Header;
