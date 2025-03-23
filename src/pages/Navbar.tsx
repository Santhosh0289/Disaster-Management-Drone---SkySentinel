import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../styles/navbar.css";

const Navbar: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Clear authentication state on reload
    localStorage.removeItem("isAuthenticated");

    // Check login status from localStorage
    const storedAuth = localStorage.getItem("isAuthenticated") === "true";
    setIsAuthenticated(storedAuth);

    // Listen for login/logout changes
    const handleStorageChange = () => {
      setIsAuthenticated(localStorage.getItem("isAuthenticated") === "true");
    };

    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, []);

  return (
    <nav className="navbar">
      <Link to="/" className="logo">Sky Sentinel</Link>
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/modes">Modes</Link>
        <Link to="/recording">Recording</Link>
        <Link to="/about">About</Link>
        {!isAuthenticated && <Link to="/login" className="login-link">Login</Link>}
      </div>
    </nav>
  );
};

export default Navbar;
