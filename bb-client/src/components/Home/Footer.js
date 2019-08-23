import PropTypes from "prop-types";
import React, { Component } from "react";
import { Segment } from "semantic-ui-react";

export default class Footer extends Component {
  state = { activeItem: "home" };

  handleItemClick = (e, { name }) => this.setState({ activeItem: name });

  componentDidMount() {}

  render() {
    const { activeItem } = this.state;

    return (
      <Segment
        textAlign="center"
        inverted
        vertical
        color="blue"
        style={{
          padding: "10px",
          position: "fixed",
          left: 0,
          bottom: 0,
          width: "100%",
          color: "white",
          textAlign: "center"
        }}
      >
        Bug Zorro {new Date().getFullYear()}
      </Segment>
    );
  }
}
