/*eslint-disable*/
import React from "react";
// used for making the prop types of this component
import PropTypes from "prop-types";

// reactstrap components
import { Container, Row, Nav, NavItem, NavLink } from "reactstrap";

class Footer extends React.Component {
  render() {
        return (
          <footer className="footer">
            <Container fluid>
              <Nav>
                <NavItem>
                  <NavLink href="/aboutus">About Us</NavLink>
                </NavItem>
              </Nav>
              <div className="copyright">
                © {new Date().getFullYear()}
                <a
                  href="javascript:void(0)"
                  rel="noopener noreferrer"
                  target="_blank"
                ></a>{" "}
              </div>
            </Container>
      </footer>
    );
  }
}

export default Footer;
