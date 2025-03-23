import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./pages/Navbar";
import Home from "./pages/Home";
import Recording from "./pages/RecordingPage";
import About from "./pages/About";
import ModeSelection from "./pages/Mode"; // Import ModeSelection page
import PrivateSurveillance from "./pages/PrivateSurveillance"; // Import PrivateSurveillance page
import MilitarySurveillance from "./pages/military";
import ResearchSurveillance from "./pages/ResearchSurveillance";
import DisasterSurveillance from "./pages/DisasterSurveillance";
import Login from "./pages/login";
import Signup from "./pages/signup"; // Import Signup page
import EnvironmentalAnalysis from "./pages/env"

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/recording" element={<Recording />} />
          <Route path="/about" element={<About />} />
          <Route path="/modes" element={<ModeSelection />} />
          <Route path="/private-surveillance" element={<PrivateSurveillance />} /> {/* Added Private Surveillance route */}
          <Route path="/military-surveillance" element={<MilitarySurveillance />} />
          <Route path="/research" element={< ResearchSurveillance/>} />
          <Route path="/disaster-response" element={< DisasterSurveillance/>} />
          <Route path="/environmental-analysis" element={<EnvironmentalAnalysis />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
