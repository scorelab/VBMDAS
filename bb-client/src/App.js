import React, { Component } from 'react'
import { BrowserRouter, Route, Switch } from "react-router-dom";
import './App.css';

import Navigation from './components/Navigation';
import Home from './components/Home';
import Page404 from './components/Page404';
import SignUp from './components/SignUp'
import SignIn from './components/SignIn'

class App extends Component {
  render() {
    return (
      <BrowserRouter>
          <Navigation/>
            <Switch>
              <Route exact path="/" component={Home}/>
              <Route path="/signup" component={SignUp} />
              <Route path="/signin" component={SignIn} />
              <Route component={Page404} />
            </Switch>
        </BrowserRouter>
    )
  }
}

export default App;
