import React from 'react';
import TextField from '@material-ui/core/TextField';
import { Autocomplete } from '@mui/material';

class SearchBar extends React.Component {
  render() {
    return (
      <Autocomplete
        id="search-bar"
        options={this.props.options}
        renderInput={(params) => (
          <TextField
            {...params}
            variant="filled"
            style={{
              backgroundColor: 'darkgrey',
              width: '500px',
              marginTop: '13px',
            }}
            placeholder="Search for a debater"
          />
        )}
        onChange={(_, value) => {
          if (value === null) return;
          const debaterCode = value.id.replaceAll(' ', '_');
          window.open(`/debater?code=${debaterCode}`, '_self');
        }}
      />
    );
  }
}

export default SearchBar;
