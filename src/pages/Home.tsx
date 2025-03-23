import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/home.css";

const Home: React.FC = () => {
  const navigate = useNavigate();
  const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";

  return (
    <div className="home">
      {/* Clouds start by covering the screen and slowly clear out */}
      <div className="clouds clouds-1"></div>
      <div className="clouds clouds-2"></div>
      <div className="clouds clouds-3"></div>

      {/* Content appears as the clouds clear */}
      <h1>Welcome to Sky Sentinel</h1>
      <p>
        Experience next-level surveillance with our advanced AI-powered drone solutions.
      </p>
      <button className="cta-button" onClick={() => navigate(isAuthenticated ? "/modes" : "/login")}>
        Explore Now
      </button>
    </div>
  );
};

export default Home;
