import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "../styles/env.css";

const FlightPaths: React.FC = () => {
  const [paths, setPaths] = useState<string[]>([]);
  const [selectedPath, setSelectedPath] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [detectedObjects, setDetectedObjects] = useState<string[]>([]);
  const videoRef = useRef<HTMLImageElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  // Fetch saved flight paths
  useEffect(() => {
    axios
      .get("http://localhost:8000/paths")
      .then((response) => {
        console.log("API Response:", response.data);
        if (response.data && Array.isArray(response.data.available_paths)) {
          setPaths(response.data.available_paths);
        } else {
          setError("Invalid response format");
        }
      })
      .catch((error) => {
        console.error("Error fetching paths:", error);
        setError("Failed to fetch paths. Please check the backend.");
      });
  }, []);

  // Start flight
  const startFlight = async (path: string) => {
    setLoading(true);
    setSelectedPath(path);
    try {
      const response = await axios.post(`http://localhost:8000/start/${path}`);
      console.log("Flight Started Response:", response.data);
    } catch (error) {
      console.error("Error starting flight:", error);
      setError("Failed to start flight");
    }
    setLoading(false);
  };

  // Stop flight
  const stopFlight = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/stop");
      console.log("Flight Stopped Response:", response.data);
      setSelectedPath(null);
    } catch (error) {
      console.error("Error stopping flight:", error);
      setError("Failed to stop flight");
    }
    setLoading(false);
  };

  // WebSocket connection for live feed
  useEffect(() => {
    if (selectedPath) {
      wsRef.current = new WebSocket("ws://localhost:8000/video");

      wsRef.current.onopen = () => console.log("WebSocket connected!");

      wsRef.current.onmessage = (event) => {
        console.log("Received data:", event.data);
        if (videoRef.current) {
          const blob = new Blob([event.data], { type: "image/jpeg" });
          const url = URL.createObjectURL(blob);
          videoRef.current.src = url;
        }
      };

      wsRef.current.onerror = (error) => {
        console.error("WebSocket error:", error);
        setError("Failed to connect to live feed.");
      };

      wsRef.current.onclose = () => {
        console.log("WebSocket connection closed.");
      };

      return () => {
        if (wsRef.current) {
          wsRef.current.close();
        }
        if (videoRef.current && videoRef.current.src) {
          URL.revokeObjectURL(videoRef.current.src);
        }
      };
    }
  }, [selectedPath]);

  // Simulated detected objects (Replace with real API response)
  useEffect(() => {
    if (selectedPath) {
      const interval = setInterval(() => {
        setDetectedObjects(["Person", "Fire", "Smoke", "Car", "Dog"]);
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [selectedPath]);

  return (
    <div className="flight-paths-container">
      <h1 className="title">SkySentinel Drone Control</h1>

      {error && <p className="error-message">{error}</p>}

      {!selectedPath ? (
        <div className="paths-grid">
          {paths.length > 0 ? (
            paths.map((path) => (
              <button
                key={path}
                onClick={() => startFlight(path)}
                disabled={loading}
                className="path-button"
              >
                {path}
              </button>
            ))
          ) : (
            <p>No saved flight paths available.</p>
          )}
        </div>
      ) : (
        <div className="live-feed-container">
          <div className="video-feed">
            <img ref={videoRef} alt="Live Feed" className="live-feed" />
          </div>
          <div className="detected-objects">
            <h2>Detected Objects</h2>
            <ul>
              {detectedObjects.map((obj, index) => (
                <li key={index}>{obj}</li>
              ))}
            </ul>
          </div>
          <button onClick={stopFlight} disabled={loading} className="stop-button">
            Stop Flight
          </button>
        </div>
      )}
    </div>
  );
};

export default FlightPaths;