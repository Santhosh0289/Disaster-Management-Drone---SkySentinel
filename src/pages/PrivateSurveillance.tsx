import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import "../styles/Surveillance.css"; // Import the common CSS file

const PrivateSurveillance: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="surveillance-container private-mode">
      {/* Overlay for Aesthetic Effect */}
      <div className="background-overlay"></div>

      {/* Header Section */}
      <motion.div 
        className="surveillance-header"
        initial={{ opacity: 0, y: -50 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 0.8 }}
      >
        <h1>Private Surveillance</h1>
        <p>AI-powered drone security monitoring for enhanced safety</p>
      </motion.div>

      {/* Grid Container for Features */}
      <div className="surveillance-grid">
        {/* Live Surveillance */}
        <motion.div 
          className="surveillance-card private"
          whileHover={{ scale: 1.07, rotate: 1 }}
        >
          <h2>Live Surveillance</h2>
          <p>Monitor real-time drone footage and capture high-resolution images.</p>
          <button className="surveillance-btn">Start Monitoring</button>
        </motion.div>

        {/* Missing Person Detection */}
        <motion.div 
          className="surveillance-card private"
          whileHover={{ scale: 1.07, rotate: -1 }}
        >
          <h2>Missing Person Detection</h2>
          <p>Locate missing individuals using AI-powered facial recognition.</p>
          <button className="surveillance-btn">Scan Now</button>
        </motion.div>

        {/* Face Recognition */}
        <motion.div 
          className="surveillance-card private"
          whileHover={{ scale: 1.07, rotate: 1 }}
        >
          <h2>Face Recognition</h2>
          <p>Identify authorized and unauthorized individuals in real-time.</p>
          <button className="surveillance-btn">Start Recognition</button>
        </motion.div>
      </div>

      {/* Circular Back Button Fixed to Bottom-Left */}
      <div className="back-btn-container">
        <motion.button 
          className="back-btn" 
          whileHover={{ scale: 1.1 }} 
          onClick={() => navigate("/modes")}
        >
          ⬅️ <span>Back to Modes</span>
        </motion.button>
      </div>
    </div>
  );
};

export default PrivateSurveillance;
