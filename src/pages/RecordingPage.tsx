import { useState } from "react";
import "../styles/recording.css";

export default function RecordingPage() {
  const [pathName, setPathName] = useState("");
  const [isTakingOff, setIsTakingOff] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [command, setCommand] = useState("");
  const [duration, setDuration] = useState(1);
  const [pathConfirmed, setPathConfirmed] = useState(false);

  // Start recording function
  const startRecording = async () => {
    if (!pathName.trim()) {
      alert("Please enter a path name.");
      return;
    }

    setPathConfirmed(true);
    setIsTakingOff(true);
    setStatusMessage("🚁 Taking off...");

    try {
      const response = await fetch("http://127.0.0.1:8000/takeoff/", { method: "POST" });
      if (!response.ok) throw new Error(`HTTP Error ${response.status}`);

      const data = await response.json();
      if (data.error) {
        setStatusMessage(`❌ ${data.error}`);
        setIsTakingOff(false);
        return;
      }

      setStatusMessage(data.message || "✅ Drone took off successfully!");
      setIsTakingOff(false);
      setIsRecording(true);
    } catch (error: any) {
      console.error("Takeoff error:", error);
      setStatusMessage(`❌ Takeoff failed: ${error.message || "Unknown error"}`);
      setIsTakingOff(false);
    }
  };

  // Function to send a command to the drone
  const sendCommand = async () => {
    if (!command.trim()) {
      alert("Please enter a command.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/execute-commands/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          path_name: pathName,
          commands: [{ cmd: command, duration: duration }],
        }),
      });

      const data = await response.json();
      setStatusMessage(data.message || `Command executed: ${command}`);
    } catch (error: any) {
      console.error("Command error:", error);
      setStatusMessage(`❌ Command failed: ${error.message || "Unknown error"}`);
    }
  };

  // Function to land the drone
  const landDrone = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/land/", { method: "POST" });
      if (!response.ok) throw new Error(`HTTP Error ${response.status}`);

      const data = await response.json();
      setStatusMessage(data.message || "🛬 Drone landed successfully!");
      setIsRecording(false);
    } catch (error: any) {
      console.error("Landing error:", error);
      setStatusMessage(`❌ Landing failed: ${error.message || "Unknown error"}`);
    }
  };

  return (
    <div className={`recording-container ${isTakingOff ? "taking-off" : ""}`}>
      <h1>Tello Drone Controller</h1>

      <div className={`video-container ${pathConfirmed ? "expanded-video" : ""}`}>
        <img className="video-feed" src="http://localhost:8000/video_feed" alt="Drone Stream" />
      </div>

      <div className="controls-wrapper">
        <div className="controls-container">
          {!pathConfirmed && (
            <div className="path-controls">
              <input
                type="text"
                placeholder="Enter new path name"
                value={pathName}
                onChange={(e) => setPathName(e.target.value)}
              />
              <button onClick={startRecording} disabled={isTakingOff || isRecording}>
                {isTakingOff ? "Taking Off..." : "Record New Path"}
              </button>
            </div>
          )}

          {isRecording && (
            <div className="command-controls">
              <h3>Enter Commands:</h3>
              <div className="command-input">
                <select value={command} onChange={(e) => setCommand(e.target.value)}>
                  <option value="">Select Command</option>
                  <option value="w">Move Forward</option>
                  <option value="s">Move Backward</option>
                  <option value="a">Move Left</option>
                  <option value="d">Move Right</option>
                  <option value="u">Move Up</option>
                  <option value="j">Move Down</option>
                  <option value="q">Rotate Counter-Clockwise</option>
                  <option value="e">Rotate Clockwise</option>
                </select>
                <input
                  type="number"
                  placeholder="Duration (seconds)"
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  min="1"
                />
                <button onClick={sendCommand}>Send Command</button>
              </div>
              <button onClick={landDrone} className="land-btn">Land Drone</button>
            </div>
          )}
        </div>

        {statusMessage && <p className="status-message">{statusMessage}</p>}
      </div>

      <button className="existing-paths-btn">Existing Paths</button>
    </div>
  );
}