import React from "react";

// TODO:
// just collect more data for 2019-2020 or maybe some 2020-2021,
// and then set up an automated process for data collection
// (dont necessarily have to use the new data)
// TODO:

class Logo extends React.Component {
  render() {
    return (
      <a href="/">
        <img
          src="logo_wide_white_text.png"
          style={{ width: "250px", position: "absolute", left: 12, top: 17 }}
        />
      </a>
    );
  }
}

export default Logo;
