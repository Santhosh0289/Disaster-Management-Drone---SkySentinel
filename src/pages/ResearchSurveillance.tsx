import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import "../styles/Surveillance.css"; // Import the common CSS file

const ResearchSurveillance: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="surveillance-container research-mode">
      {/* Overlay for Aesthetic Look */}
      <div className="background-overlay"></div>

      {/* Header Section */}
      <motion.div 
        className="surveillance-header"
        initial={{ opacity: 0, y: -50 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 0.8 }}
      >
        <h1>Research Surveillance</h1>
        <p>AI-powered drone monitoring for environmental & scientific research</p>
      </motion.div>

      {/* Grid Container for Features */}
      <div className="surveillance-grid">
        {/* Environmental Analysis */}
        <motion.div 
          className="surveillance-card research"
          whileHover={{ scale: 1.07, rotate: 1 }}
        >
          <h2>Environmental Analysis</h2>
          <p>Collect real-time environmental data for scientific research.</p>
          <button className="surveillance-btn" onClick={() => navigate("/environmental-analysis")}>Start Analysis</button>
        </motion.div>

        {/* Wildlife Tracking */}
        <motion.div 
          className="surveillance-card research"
          whileHover={{ scale: 1.07, rotate: -1 }}
        >
          <h2>Wildlife Tracking</h2>
          <p>Monitor and track animal movement using AI-powered drones.</p>
          <button className="surveillance-btn">Track Now</button>
        </motion.div>

        {/* Anomaly Detection */}
        <motion.div 
          className="surveillance-card research"
          whileHover={{ scale: 1.07, rotate: 1 }}
        >
          <h2>Anomaly Detection</h2>
          <p>Detect new objects or subjects and capture 360-degree photos.</p>
          <button className="surveillance-btn">Start Scanning</button>
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

export default ResearchSurveillance;