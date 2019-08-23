import React, { Component } from "react";
import { Menu, Dropdown, Icon } from "semantic-ui-react";
import { BrowserRouter as Link, NavLink } from "react-router-dom";
import { signOut } from "../../store/actions";
import { connect } from "react-redux";
import PropTypes from "prop-types";

class Navbar extends Component {
  //log out via dispatch
  onLogoutClick(e) {
    e.preventDefault();
    this.props.logout();
  }
  state = { activeItem: "home" };

  handleItemClick = (e, { name }) => this.setState({ activeItem: name });

  render() {
    const { activeItem } = this.state;
    const { logged, userName, orgFlag, hackerFlag } = this.props;

    return (
      <div>
        <Menu color="blue" fixed="top" inverted style={{ height: "60px" }}>
          <Menu.Item
            as={NavLink}
            content="Bug Zorro"
            to=""
            style={{ fontSize: "30px", fontWeight: "bold" }}
          />
          {logged === true ? (
            <>
              <Menu.Item
                as={NavLink}
                content="Hackactivity"
                to="hackactivity"
                active={activeItem === "hackactivity"}
                onClick={this.handleItemClick}
              />
              <Menu.Item
                as={NavLink}
                content="Programs"
                to="programs"
                active={activeItem === "programs"}
                onClick={this.handleItemClick}
              />
              {/* only show the Hacker Dashboard menu item if the logged in user is a hacker user */}
              {orgFlag === false && hackerFlag === true ? (
                <Menu.Item
                  as={NavLink}
                  content="Hacker Dashboard"
                  to="hackerdashboard"
                  active={activeItem === "hackerdashboard"}
                  onClick={this.handleItemClick}
                />
              ) : null}
              {/* only show the Programs Dashboard and Programs Settings menu items if the logged in user is an org user */}
              {orgFlag === true && hackerFlag === false ? (
                <>
                  <Menu.Item
                    as={NavLink}
                    content="Programs Dashboard"
                    to="programsdashboard"
                    active={activeItem === "programsdashboard"}
                    onClick={this.handleItemClick}
                  />
                  <Menu.Item
                    as={NavLink}
                    content="Programs Settings"
                    to="programssettings"
                    active={activeItem === "programssettings"}
                    onClick={this.handleItemClick}
                  />
                </>
              ) : null}
            </>
          ) : null}
          {logged === true ? (
            <Menu.Menu position="right">
              <Menu.Item as={NavLink} to="messages">
                <Icon name="envelope" />
              </Menu.Item>
              <Menu.Item as={NavLink} to="profile">
                <Icon name="user" />
              </Menu.Item>
              <Dropdown item text={userName} style={{ marginRight: "60px" }}>
                <Dropdown.Menu>
                  <Dropdown.Item>Profile</Dropdown.Item>
                  <Dropdown.Item>Settings</Dropdown.Item>
                  <Dropdown.Item onClick={this.onLogoutClick.bind(this)}>
                    Sign Out
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </Menu.Menu>
          ) : (
            <Menu.Menu position="right">
              <Menu.Item as={NavLink} content="Log In" to="signin" />
              <Menu.Item
                as={NavLink}
                content="Sign Up"
                to="signup"
                style={{ marginRight: "60px" }}
              />
            </Menu.Menu>
          )}
        </Menu>
      </div>
    );
  }
}

Navbar.propTypes = {
  logged: PropTypes.bool.isRequired,
  logout: PropTypes.func.isRequired,
  userName: PropTypes.string,
  orgFlag: PropTypes.bool,
  hackerFlag: PropTypes.bool
};

const mapStateToProps = ({ auth }) => ({
  orgFlag: auth.flag.org,
  hackerFlag: auth.flag.hacker
});

const mapDispatchToProps = {
  logout: signOut
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Navbar);
