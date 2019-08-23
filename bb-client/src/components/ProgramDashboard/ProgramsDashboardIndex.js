import React, { Component } from "react";
import Footer from "./../home/Footer";
import Navbar from "./../home/Navbar";
import { connect } from "react-redux";

class ProgramsDashboard extends Component {
  render() {
    //get auth data from props
    const { loggedIn, email } = this.props;

    return (
      <div>
        <Navbar logged={loggedIn} userName={email} />
        HackActivity
        <Footer />
        <h1 style={{ marginTop: "80px" }}>Programs Dashboard Works</h1>
      </div>
    );
  }
}

const mapStateToProps = ({ firebase }) => ({
  loggedIn: firebase.auth.uid ? true : false,
  email: firebase.auth.email ? firebase.auth.email : null
});

export default connect(mapStateToProps)(ProgramsDashboard);
