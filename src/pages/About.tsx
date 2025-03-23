import React from "react";
import "../styles/about.css"; // Ensure this file contains the latest CSS

const About: React.FC = () => {
    return (
        <div className="about-container">
            {/* Header Section */}
            <h1 className="about-header">About Sky Sentinel</h1>
            <p className="about-subtitle">
                Sky Sentinel is an AI-powered surveillance drone system designed for real-time monitoring, facial recognition, environmental analysis, and path recording. 
                It provides high-precision intelligence across security, military, research, and disaster response operations.
            </p>

            {/* Introduction Section */}
            <section className="about-section">
                <h2 className="about-title">What is Sky Sentinel?</h2>
                <p className="about-text">
                    Sky Sentinel is an advanced autonomous drone system that integrates AI, computer vision, and real-time data analytics to provide next-generation surveillance solutions. 
                    With multiple operational modes, it adapts to diverse security and research applications.
                </p>
            </section>

            {/* Features Section */}
            <section className="about-section">
                <h2 className="about-title">Core Features</h2>
                <ul className="about-list">
                    <li>AI-driven real-time surveillance</li>
                    <li>Facial and anomaly recognition with OpenCV and TensorFlow</li>
                    <li>GPS-based path recording and autonomous navigation</li>
                    <li>Live data streaming with WebSocket support</li>
                    <li>Environmental monitoring for research and disaster response</li>
                    <li>Secure and privacy-focused cloud integration</li>
                </ul>
            </section>

            {/* Application Modes Section */}
            <section className="about-section">
                <h2 className="about-title">Application Areas</h2>
                <div className="about-grid">
                    <div className="about-box">
                        <h3>Private Security</h3>
                        <p>Protects residential, commercial, and industrial properties with AI-powered surveillance drones capable of continuous monitoring.</p>
                    </div>
                    <div className="about-box">
                        <h3>Military and Defense</h3>
                        <p>Enhances battlefield awareness with autonomous reconnaissance and real-time threat detection.</p>
                    </div>
                    <div className="about-box">
                        <h3>Scientific Research</h3>
                        <p>Assists in environmental monitoring, climate studies, and remote exploration through aerial data collection.</p>
                    </div>
                    <div className="about-box">
                        <h3>Disaster Response</h3>
                        <p>Supports search and rescue operations, fire detection, and emergency response by providing real-time situational awareness.</p>
                    </div>
                </div>
            </section>

            {/* Future Vision Section */}
            <section className="about-section">
                <h2 className="about-title">Future Enhancements</h2>
                <p className="about-future">
                    Sky Sentinel is continuously evolving to integrate advanced AI-driven decision-making, cloud-based flight path sharing, and enhanced 3D mapping. 
                    The platform aims to set new standards in autonomous aerial intelligence and real-time surveillance technology.
                </p>
            </section>
        </div>
    );
};

export default About;
