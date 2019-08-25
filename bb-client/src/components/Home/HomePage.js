import PropTypes from "prop-types";
import React, { Component } from "react";
import Footer from "./Footer";
import Navbar from "./Navbar";

import { connect } from "react-redux";
const imageStyle = {
  align: "center"
};
class HomePage extends Component {
  render() {
    //get auth data from props
    const { loggedIn, email } = this.props;
    return (
      <div>
        <Navbar logged={loggedIn} userName={email} />
        <br />
        <br />
        <br />
        Home Page
        <Footer />
      </div>
    );
  }
}

const mapStateToProps = ({ firebase }) => ({
  loggedIn: firebase.auth.uid ? true : false,
  email: firebase.auth.email ? firebase.auth.email : null
});

export default connect(mapStateToProps)(HomePage);
