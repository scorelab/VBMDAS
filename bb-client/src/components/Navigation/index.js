import React, { Component } from "react";
import { Menu, Container } from "semantic-ui-react";
import { Link, withRouter } from "react-router-dom";

const fixedMenuStyle = {
  backgroundColor: '#fff',
  border: '1px solid #ddd',
  boxShadow: '0px 3px 5px rgba(0, 0, 0, 0.2)',
}

class Navigation extends Component {
  render() {
    return (
      <Menu borderless fixed='top' style={fixedMenuStyle}>
        <Container text>
          <Menu.Item header as={Link} to='/'>
            B Bounty
          </Menu.Item>
          <Menu.Menu position="right">
            <Menu.Item position="right" as={Link} to='/signin'>
              Sign In
            </Menu.Item>
            <Menu.Item position="right" as={Link} to='/signup'>
              Sign Up
            </Menu.Item>
          </Menu.Menu>
        </Container>
      </Menu>
    );
  }
}

export default withRouter(Navigation);
