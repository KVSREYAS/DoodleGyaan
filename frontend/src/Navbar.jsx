import React from 'react';
import './Navbar.css'; // Make sure to create a corresponding CSS file for styling
import logo from './assets/logo.png'; // Make sure to import the logo image

function Navbar() {
  return (
    <div className = "parent">
        <nav className="navbar">
        <div className="navbar-left">
            <a href="/"><img src={logo} alt="Logo" className="navbar-icon" /></a>
        </div>
        <div className="navbar-center">
            <a href="/generate" className="navbar-link">Generate</a>
            <a href="/catalog" className="navbar-link">Catalog</a>
            <a href="/cotd" className="navbar-link">Comic of the Day</a>
            <a href="/about" className="navbar-link">About Us</a>
        </div>
        <div className="navbar-right">
            <a href="/login" className="navbar-login">Login</a>
            <a href="/signup" className="navbar-signup">Sign Up</a>
        </div>
        </nav>
    </div>
  );
}

export default Navbar;