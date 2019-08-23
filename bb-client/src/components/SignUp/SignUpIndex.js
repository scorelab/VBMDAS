import React, { Component } from "react";
import Footer from "./../home/Footer";
import Navbar from "./../home/Navbar";
import * as EmailValidator from "email-validator";
import * as actions from "../../store/actions";
import { connect } from "react-redux";
import validator from "validator";
import { NavLink } from "react-router-dom";

class SignUp extends Component {
  constructor(props) {
    super(props);

    this.state = {
      signUpMethod: "hacker",
      check: false,
      hk_name: "",
      hk_email: "",
      hk_password: "",
      hk_confirm_password: "",
      org_name: "",
      org_website: "",
      org_full_name: "",
      org_email: "",
      org_password: "",
      org_confirm_password: ""
    };
  }

  changeState(type) {
    this.setState({
      signUpMethod: type,
      check: false
    });
  }

  changeCheckStatus = () => {
    const tmp = this.state.check;
    this.setState({ check: !tmp });
    console.log(this.state.hk_name);
  };

  //redux reducer actions declared in ../../store/actions
  registerHacker = e => {
    const {
      hk_name,
      hk_email,
      hk_password,
      hk_confirm_password,
      check
    } = this.state;
    if (EmailValidator.validate(hk_email) === true) {
      if (check) {
        if (hk_password === hk_confirm_password) {
          e.preventDefault();
          const userData = {
            hk_name,
            hk_email,
            hk_password
          };
          this.props.signUpHacker(userData, this.props.history); //when the user is logged in redirect to sign in page
        } else {
          alert("Password mismatch. Retype the passwords correctly");
          this.setState({
            hk_password: "",
            hk_confirm_password: ""
          });
          e.preventDefault();
        }
      } else {
        alert("Please read the privacy policies and Accept them");
        e.preventDefault();
      }
    } else {
      alert(
        "Your email is not a valid email. Please insert valid email address"
      );
      e.preventDefault();
    }
  };

  //redux reducer actions declared in ../../store/actions
  registerOrganization = e => {
    const {
      org_name,
      org_email,
      org_website,
      org_full_name,
      org_password,
      org_confirm_password
    } = this.state;
    if (EmailValidator.validate(org_email) === true) {
      if (org_password === org_confirm_password) {
        if (validator.isURL(this.state.org_website)) {
          e.preventDefault();
          const orgData = {
            org_name,
            org_email,
            org_website,
            org_full_name,
            org_password
          };
          this.props.signUpOrg(orgData, this.props.history); //when the orguser is logged in redirect to sign in page
        } else {
          e.preventDefault();
          this.setState({ org_website: "" });
          alert("Organization website URL is not valid. Please check the URL");
        }
      } else {
        alert("Password mismatch. Retype the passwords correctly");
        this.setState({
          org_password: "",
          org_confirm_password: ""
        });
        e.preventDefault();
      }
    } else {
      alert(
        "Your email is not a valid email. Please insert valid emali address"
      );
      e.preventDefault();
    }
  };

  render() {
    return (
      <div>
        <Navbar logged={false} />
        <div
          style={{
            marginLeft: "30%",
            width: "40%",
            background: "#1991EB",
            padding: "3%",
            marginTop: "1%"
          }}
        >
          <div
            style={{
              color: "white",
              marginLeft: "30%",
              fontFamily: "Lato",
              fontWeight: "800",
              fontsize: "50px",
              lineHeight: "21px"
            }}
          >
            <b>Welcome to the Bug Zorro</b>
          </div>
          <div className="ui two top attached buttons">
            <div
              className="ui button"
              style={{
                background: "#1991EB",
                display: "flex",
                color: "white",
                fontWeight: "800",
                fontsize: "50px",
                lineHeight: "21px",
                alignItems: "center"
              }}
              onClick={() => this.changeState("hacker")}
            >
              Sign Up as a Hacker
            </div>
            <div
              className="ui button"
              style={{
                background: "#1991EB",
                color: "white",
                fontWeight: "800",
                fontsize: "50px",
                lineHeight: "21px"
              }}
              onClick={() => this.changeState("programme")}
            >
              Create a Program
            </div>
          </div>
          {this.state.signUpMethod === "hacker" ? (
            <form className="ui form" onSubmit={this.registerHacker}>
              <div
                className="ui left icon input"
                style={{ width: "95%", margin: "2%" }}
              >
                <input
                  type="text"
                  name="name"
                  placeholder="Your Name"
                  value={this.state.hk_name}
                  onChange={event =>
                    this.setState({ hk_name: event.target.value })
                  }
                  required
                />
                <i className="info circle icon" />
              </div>
              <div
                className="ui left icon input"
                style={{ width: "95%", margin: "2%" }}
              >
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={this.state.hk_email}
                  onChange={event =>
                    this.setState({ hk_email: event.target.value })
                  }
                  required
                />
                <i className="envelope icon" />
              </div>
              <div
                className="ui left icon input"
                style={{ width: "95%", margin: "2%" }}
              >
                <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={this.state.hk_password}
                  onChange={event =>
                    this.setState({ hk_password: event.target.value })
                  }
                  required
                />
                <i className="key icon" />
              </div>
              <div
                className="ui left icon input"
                style={{ width: "95%", margin: "2%" }}
              >
                <input
                  type="password"
                  name="confirmPassword"
                  placeholder="Confirm Password"
                  value={this.state.hk_confirm_password}
                  onChange={event =>
                    this.setState({ hk_confirm_password: event.target.value })
                  }
                  required
                />
                <i className="key icon" />
              </div>
              <div className="field" style={{ width: "95%", margin: "2%" }}>
                <div className="ui checkbox">
                  <input
                    type="checkbox"
                    name="privacy_policy"
                    onChange={this.changeCheckStatus}
                  />
                  <label style={{ color: "white", fontFamily: "Lato" }}>
                    I Agree To Bug Zorro's Terms And Conditions And Acknowledge
                    That I Have Read The Privacy Policy
                  </label>
                </div>
              </div>
              <button
                className="ui button"
                type="submit"
                style={{ fontFamily: "Lato", width: "95%", marginLeft: "2%" }}
              >
                Create Account
              </button>
              <div
                style={{
                  alignItems: "center",
                  position: "absolute",
                  width: "100%",
                  marginTop: "2%",
                  marginLeft: "27%",
                  marginBottom: "2%"
                }}
              >
                <label style={{ color: "white", fontFamily: "Lato" }}>
                  Already created an account?
                </label>
                <NavLink style={{ whiteSpace: "unset" }} to="/signin">
                  <label> Sign in here.</label>
                </NavLink>
              </div>
            </form>
          ) : (
            <form className="ui form" onSubmit={this.registerOrganization}>
              <div
                className="ui left icon input"
                style={{ width: "95%", margin: "2%" }}
              >
                <input
                  type="text"
                  name="org_name"
                  placeholder="Organization Name"
                  value={this.state.org_name}
                  onChange={event =>
                    this.setState({ org_name: event.target.value })
                  }
                  required
                />
                <i className="info circle icon" />
              </div>
              <div
                className="ui left icon input"
                style={{ width: "95%", margin: "2%" }}
              >
                <input
                  type="text"
                  name="website"
                  placeholder="Website"
                  value={this.state.org_website}
                  onChange={event =>
                    this.setState({ org_website: event.target.value })
                  }
                  required
                />
                <i className="info circle icon" />
              </div>
              <div
                className="ui left icon input"
                style={{ width: "95%", margin: "2%" }}
              >
                <input
                  type="text"
                  name="full_name"
                  placeholder="Full Name"
                  value={this.state.org_full_name}
                  onChange={event =>
                    this.setState({ org_full_name: event.target.value })
                  }
                  required
                />
                <i className="info circle icon" />
              </div>
              <div
                className="ui left icon input"
                style={{ width: "95%", margin: "2%" }}
              >
                <input
                  type="email"
                  name="org_email"
                  placeholder="Email"
                  value={this.state.org_email}
                  onChange={event =>
                    this.setState({ org_email: event.target.value })
                  }
                  required
                />
                <i className="envelope icon" />
              </div>
              <div
                className="ui left icon input"
                style={{ width: "95%", margin: "2%" }}
              >
                <input
                  type="password"
                  name="org_password"
                  placeholder="Password"
                  value={this.state.org_password}
                  onChange={event =>
                    this.setState({ org_password: event.target.value })
                  }
                  required
                />
                <i className="key icon" />
              </div>
              <div
                className="ui left icon input"
                style={{ width: "95%", margin: "2%" }}
              >
                <input
                  type="password"
                  name="org_confirmPassword"
                  placeholder="Confirm Password"
                  value={this.state.org_confirm_password}
                  onChange={event =>
                    this.setState({ org_confirm_password: event.target.value })
                  }
                  required
                />
                <i className="key icon" />
              </div>
              <button
                className="ui button"
                type="submit"
                style={{ fontFamily: "Lato", width: "95%", margin: "2%" }}
              >
                Create Program
              </button>
              <div style={{ width: "95%", marginLeft: "2%" }}>
                <label style={{ color: "white" }}>
                  By clicking 'Create Program', you agree to our Terms and
                  Conditions and acknowledge that you have read our Privacy
                  Policy and Disclosure Guidelines
                </label>
              </div>
            </form>
          )}
        </div>
        <Footer />
      </div>
    );
  }
}

const mapDispatchToProps = {
  signUpHacker: actions.signUpHacker,
  signUpOrg: actions.signUpOrg
};

export default connect(
  null,
  mapDispatchToProps
)(SignUp);
