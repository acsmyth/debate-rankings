import React from "react";

class Logo extends React.Component {
  render() {
    return (
      <a href="/">
        <img
          src="logo_wide_white_text.png"
          style={{ width: "250px", position: "absolute", left: 12, top: 17 }}
          alt="Debate Rankings"
        />
      </a>
    );
  }
}

export default Logo;
