import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate for navigation
import { motion } from "framer-motion";
import "../styles/Mode.css";
import securityImage from "../images/security.webp";
import militaryImage from "../images/military.jpg";
import researchImage from "../images/research.jpg";
import disasterImage from "../images/disaster.png";

const modes = [
  { name: "Private Security", image: securityImage, route: "/private-surveillance" },
  { name: "Military", image: militaryImage, route: "/military-surveillance" }, // Fixed route
  { name: "Research", image: researchImage, route: "/research" },
  { name: "Disaster Response", image: disasterImage, route: "/disaster-response" },
];

export default function ModeSelection() {
  const [hoveredMode, setHoveredMode] = useState<string | null>(null);
  const navigate = useNavigate(); // React Router navigation

  return (
    <div className="mode-container">
      <h1 className="mode-title">Select a Mode</h1>
      <div className="mode-circle-container">
        {modes.map((mode, index) => (
          <motion.div
            key={index}
            className="mode-circle"
            onMouseEnter={() => setHoveredMode(mode.image)}
            onMouseLeave={() => setHoveredMode(null)}
            whileHover={{ scale: 1.15 }}
            onClick={() => navigate(mode.route)} // Navigate to respective mode page
          >
            <img src={mode.image} alt={mode.name} className="mode-image" />
            <span className="mode-text">{mode.name}</span>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
