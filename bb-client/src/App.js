import React, { Suspense, Component } from "react";
import { Route, Switch, Redirect } from "react-router-dom";
import { connect } from "react-redux";
import "./index.css";
import "semantic-ui-css/semantic.min.css";
import HomePage from "./components/home/HomePage";
import SiginIn from "./components/Signin/SignInIndex";
import SignUp from "./components/Signup/SignUpIndex";
import ForgotPassword from "./components/ForgotPassword/ForgotPasswordIndex";
import { addFlag } from "./store/actions";
import Spinner from "./helpers/Spinner";

import HackActivity from "./components/HackActivity/HackActivityIndex";
import Programs from "./components/Programs/ProgramsIndex";
import ProgramsDashboard from "./components/ProgramDashboard/ProgramsDashboardIndex";
import ProgramsSettings from "./components/ProgramsSettings/ProgramsSettingsIndex";
import HackerDashboard from "./components/HackerDashboard/HackerDashboardIndex";

class App extends Component {
  componentDidMount() {
    this.props.addFlag();
  }

  render() {
    const { loggedIn, emailVerified, orgFlag, hackerFlag } = this.props;
    let routes;

    if (loggedIn && !emailVerified) {
      routes = (
        <Switch>
          <Route exact path="/" component={HomePage} />
          <Route exact path="/signup" component={SignUp} />
          <Route exact path="/forgotpassword" component={ForgotPassword} />
          <Route exact path="/signin" component={SiginIn} />
          <Redirect to="/signin" />
        </Switch>
      );
    } else if (loggedIn && emailVerified) {
      if (hackerFlag === true && orgFlag === false) {
        routes = (
          <Suspense fallback={<Spinner />}>
            <Switch>
              <Route exact path="/" component={HomePage} />
              <Route
                exact
                path="/hackerdashboard"
                component={HackerDashboard}
              />
              <Route exact path="/programs" component={Programs} />
              <Route exact path="/hackactivity" component={HackActivity} />
              <Redirect to="/hackerdashboard" />
            </Switch>
          </Suspense>
        );
      } else if (hackerFlag === false && orgFlag === true) {
        routes = (
          <Suspense fallback={<Spinner />}>
            <Switch>
              <Route exact path="/" component={HomePage} />
              <Route
                exact
                path="/programsdashboard"
                component={ProgramsDashboard}
              />
              <Route exact path="/hackactivity" component={HackActivity} />
              <Route exact path="/programs" component={Programs} />
              <Route
                exact
                path="/programssettings"
                component={ProgramsSettings}
              />
              <Redirect to="/programsdashboard" />
            </Switch>
          </Suspense>
        );
      } else {
        routes = <Spinner />;
      }
    } else {
      routes = (
        <Switch>
          <Route exact path="/" component={HomePage} />
          <Route exact path="/signin" component={SiginIn} />
          <Route exact path="/signup" component={SignUp} />
          <Route exact path="/forgotpassword" component={ForgotPassword} />
          <Redirect to="/signin" />
        </Switch>
      );
    }

    return <div>{routes}</div>;
  }
}

const mapStateToProps = ({ firebase, auth }) => ({
  loggedIn: firebase.auth.uid,
  emailVerified: firebase.auth.emailVerified,
  orgFlag: auth.flag.org,
  hackerFlag: auth.flag.hacker
});

const mapDispatchToProps = {
  addFlag: addFlag
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(App);
