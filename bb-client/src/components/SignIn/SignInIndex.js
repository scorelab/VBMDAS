import React, { Component } from "react";
import Footer from "./../home/Footer";
import Navbar from "./../home/Navbar";
import * as EmailValidator from "email-validator";
import { NavLink } from "react-router-dom";
import * as actions from "../../store/actions";
import { connect } from "react-redux";

class SignIn extends Component {
  constructor(props) {
    super(props);

    this.state = {
      email: "",
      password: "",
      error: false,
      errorMessage: ""
    };
  }

  login = e => {
    e.preventDefault();
    let email = this.state.email;
    let password = this.state.password;
    const userData = {
      email,
      password
    };
    if (EmailValidator.validate(email) === true) {
      this.props.logIn(userData, this.props.history); //when the user is logged in redirect to dashboard
    } else {
      alert(
        "Your email is not a valid email. Please insert valid email address"
      );
      e.preventDefault();
    }
  };

  render() {
    const { error } = this.props; //getting errors from props retrieving from redux store

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
          {error ? (
            <div className="ui message">
              <div className="header">Error</div>
              <p>{error}</p>
            </div>
          ) : (
            <div />
          )}

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
            <b>Sign In to the Bug Zorro</b>
          </div>

          <form className="ui form" onSubmit={this.login}>
            <div
              className="ui left icon input"
              style={{ width: "95%", margin: "2%" }}
            >
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={this.state.email}
                onChange={event =>
                  this.setState({
                    email: event.target.value,
                    error: false,
                    errorMessage: ""
                  })
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
                value={this.state.password}
                onChange={event =>
                  this.setState({
                    password: event.target.value,
                    error: false,
                    errorMessage: ""
                  })
                }
                required
              />
              <i className="key icon" />
            </div>
            <div className="field" style={{ width: "95%", margin: "2%" }}>
              <div style={{ float: "right" }}>
                <NavLink
                  to="/forgotpassword"
                  style={{ color: "white", fontFamily: "Lato" }}
                >
                  Forgot Password ?
                </NavLink>
              </div>
            </div>
            <button
              className="ui button"
              type="submit"
              style={{ fontFamily: "Lato", width: "95%", marginLeft: "2%" }}
            >
              Sign In
            </button>
            <div
              style={{
                alignItems: "center",
                display: "flex",
                justifyContent: "center",
                width: "100%",
                marginTop: "2%",
                marginBottom: "2%",
                whiteSpace: "unset"
              }}
            >
              <label style={{ color: "white", fontFamily: "Lato" }}>
                Create a BugZorro account?&nbsp;
              </label>

              <NavLink style={{ whiteSpace: "unset" }} to="/signup">
                {" "}
                Sign Up here.
              </NavLink>
            </div>
          </form>
        </div>
        <Footer />
      </div>
    );
  }
}

const mapStateToProps = ({ auth }) => ({
  loading: auth.loading,
  error: auth.error
});

const mapDispatchToProps = {
  logIn: actions.signIn,
  cleanUp: actions.clean
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(SignIn);
