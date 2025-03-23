import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import "../styles/Surveillance.css"; // Import the common CSS file

const MilitarySurveillance: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="surveillance-container military-mode">
      {/* Overlay for Aesthetic Look */}
      <div className="background-overlay"></div>

      {/* Header Section */}
      <motion.div 
        className="surveillance-header"
        initial={{ opacity: 0, y: -50 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 0.8 }}
      >
        <h1>Military Surveillance</h1>
        <p>AI-powered tactical drone monitoring for enhanced defense</p>
      </motion.div>

      {/* Grid Container for Features */}
      <div className="surveillance-grid">
        {/* Battlefield Reconnaissance */}
        <motion.div 
          className="surveillance-card military"
          whileHover={{ scale: 1.07, rotate: 1 }}
        >
          <h2>Battlefield Recon</h2>
          <p>Monitor enemy movements and gather intelligence in real time.</p>
          <button className="surveillance-btn">Start Recon</button>
        </motion.div>

        {/* Threat Detection */}
        <motion.div 
          className="surveillance-card military"
          whileHover={{ scale: 1.07, rotate: -1 }}
        >
          <h2>Threat Detection</h2>
          <p>Detect potential threats using AI-based object recognition.</p>
          <button className="surveillance-btn">Scan for Threats</button>
        </motion.div>

        {/* Autonomous Patrol */}
        <motion.div 
          className="surveillance-card military"
          whileHover={{ scale: 1.07, rotate: 1 }}
        >
          <h2>Autonomous Patrol</h2>
          <p>Deploy AI-controlled drones for automated perimeter security.</p>
          <button className="surveillance-btn">Start Patrol</button>
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

export default MilitarySurveillance;
