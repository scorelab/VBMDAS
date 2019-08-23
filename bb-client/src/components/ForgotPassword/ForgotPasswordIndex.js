import React, { Component } from "react";
import Footer from "./../home/Footer";
import Navbar from "./../home/Navbar";
export default class ForgotPassword extends Component {
  render() {
    return (
      <div>
        <Navbar logged={false} />
        <br />
        <br />
        <br />
        ForgotPassword Page
        <Footer />
      </div>
    );
  }
}
