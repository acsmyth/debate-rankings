import React from 'react';
import Logo from './Logo';
import SearchBar from './SearchBar';
import './Header.css';

class Header extends React.Component {
  buildOptions = () => {
    return this.props.rankingsData
      .map((ranking) => ({
        label: `${ranking.code} (${ranking.name})`,
        id: ranking.code,
      }))
      .sort((a, b) => a.label.localeCompare(b.label));
  };

  render() {
    return (
      <div className="header">
        <Logo />
        <SearchBar options={this.buildOptions()} />
        <a href="https://github.com/acsmyth/debate-rankings" target="_blank">
          <img src="github_logo.svg" width="30" />
        </a>
      </div>
    );
  }
}

export default Header;
