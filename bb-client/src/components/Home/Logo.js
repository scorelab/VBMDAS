import React from "react";
import { Image, Grid } from "semantic-ui-react";
import logo from "./images/logo.png";

const LogoImage = () => (
  <Image src={logo} size="small" centered style={{ marginLeft: "500px" }} />
);
export default LogoImage;
