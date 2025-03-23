import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import "../styles/Surveillance.css"; // Import the common CSS file

const DisasterSurveillance: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="surveillance-container disaster-mode">
      {/* Overlay for Aesthetic Look */}
      <div className="background-overlay"></div>

      {/* Header Section */}
      <motion.div 
        className="surveillance-header"
        initial={{ opacity: 0, y: -50 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 0.8 }}
      >
        <h1>Disaster Response</h1>
        <p>AI-powered drone surveillance for emergency rescue and damage assessment</p>
      </motion.div>

      {/* Grid Container for Features */}
      <div className="surveillance-grid">
        {/* Search & Rescue */}
        <motion.div 
          className="surveillance-card disaster"
          whileHover={{ scale: 1.07, rotate: 1 }}
        >
          <h2>Search & Rescue</h2>
          <p>Locate missing persons and survivors using AI-driven aerial scanning.</p>
          <button className="surveillance-btn">Start Search</button>
        </motion.div>

        {/* Damage Assessment */}
        <motion.div 
          className="surveillance-card disaster"
          whileHover={{ scale: 1.07, rotate: -1 }}
        >
          <h2>Damage Assessment</h2>
          <p>Evaluate disaster impact with high-resolution aerial mapping.</p>
          <button className="surveillance-btn">Assess Damage</button>
        </motion.div>

        {/* Supply Drop Assistance */}
        <motion.div 
          className="surveillance-card disaster"
          whileHover={{ scale: 1.07, rotate: 1 }}
        >
          <h2>Supply Drop Assistance</h2>
          <p>Deliver emergency aid packages to critical areas efficiently.</p>
          <button className="surveillance-btn">Deploy Aid</button>
        </motion.div>
      </div>

      {/* Back Button */}
      <motion.div 
        className="back-btn-container"
        initial={{ opacity: 0, y: 20 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 0.6 }}
      >
        <motion.button 
          className="back-btn" 
          whileHover={{ scale: 1.1 }} 
          onClick={() => navigate("/modes")}
        >
          ← <span>Back to Modes</span>
        </motion.button>
      </motion.div>
    </div>
  );
};

export default DisasterSurveillance;
