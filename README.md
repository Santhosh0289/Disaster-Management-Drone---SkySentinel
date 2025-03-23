# Disaster-Management-Drone---SkySentinel

## 🚀 Overview
Sky Sentinel is an AI-powered flight control system designed for autonomous drone navigation, object detection, and disaster mapping. It enables **GPS-independent navigation**, **AI-driven environmental analysis**, and **multi-drone coordination** for large-scale operations. This system is built with **FastAPI, YOLOv8, and Pygame**, supporting real-time analytics and scalable deployments. 

## ⚠️ Challenges
### 🔹 Real-World Example: Himalayan Landslide
The drone will monitor and surveil the damaged areas caused by a Himalayan landslide. Equipped with advanced AI-driven object detection and mapping capabilities, it will provide real-time surveillance and analysis of the affected regions. The collected data will be forwarded to the UI, allowing disaster response teams to assess the extent of damage, locate missing persons, and optimize rescue operations efficiently.

## 📌 Key Features
- **Facial Recognition for Missing Persons** 🏥  
  The drone is equipped with an AI-based facial recognition system that can help identify missing persons in disaster-stricken areas. By scanning faces and cross-referencing them with a database, the system enhances search and rescue operations.
- **Fire & Smoke Detection** 🔥  
  Using thermal imaging and AI-driven object detection, the drone can quickly detect and locate fires in forests, buildings, or industrial areas, providing crucial early warnings for firefighting teams.
- **Damage Assessment Using 3D Mapping** 🏗️  
  The system creates high-resolution 3D maps of affected areas using aerial imagery, allowing urban planners and disaster response teams to assess structural damage and plan reconstruction efficiently.
- **Air Quality & Toxic Gas Detection** 🌫️  
  Equipped with advanced sensors and AI models, the drone can monitor air quality, detecting toxic gases, pollution levels, and hazardous conditions, which is vital for environmental and public health safety.
- **Environmental Analysis**  
  The drone continuously collects and analyzes environmental data, including temperature, humidity, and atmospheric conditions, assisting in climate research, pollution monitoring, and disaster prevention.
- **Autonomous Search Routes**  
  The drone is capable of autonomously determining search routes based on AI-driven path optimization. This ensures efficient area coverage for search and rescue missions, minimizing redundant flight paths and improving response times in critical situations.

## 🌟 Novelty
- **No-Sensor System** – Unlike traditional drones that require expensive sensors, DroneControl relies on AI models and computer vision techniques to process visual and environmental data, reducing hardware costs and increasing scalability.
- **Optimized AI Training** – The AI model has been trained extensively to achieve superior accuracy and precision in detecting objects, identifying hazards, and mapping terrain, ensuring reliable performance in various conditions.
- **Universal SDK Software** – A versatile software development kit (SDK) enables seamless connectivity between the drone and the UI using WiFi, ensuring smooth data transmission and user control.
- **GPS-Free Area Mapping** – The drone employs AI-powered algorithms to navigate and map terrain without relying on GPS, making it suitable for remote or signal-blocked areas where GPS is unavailable.
- **Endangered Species Monitoring** – The drone’s facial recognition system can identify and track endangered species in wildlife conservation efforts, providing valuable insights for researchers and helping prevent illegal poaching activities.

## ⚠️ Limitations of Existing Systems
- **High Power Consumption** – Traditional drone systems require a large amount of power to process real-time AI computations and sustain prolonged flight, which can limit operational efficiency and battery life.
- **Not Cost-Efficient** – Implementing advanced AI models, real-time processing, and high-performance networking can increase the overall cost, making widespread deployment challenging.
- **Complex Control System** – Autonomous drones require sophisticated calibration and expertise to operate efficiently, posing a challenge for widespread adoption and usability.

These are the main three limitations we are working to overcome in this project by optimizing AI models, enhancing power efficiency, and simplifying drone control mechanisms.

## ⚙️ Requirements
- Python 3.8+
- Node.js 16+
- FastAPI
- ReactJS
- YOLOv8
- OpenCV
- Pygame
- Google Maps API
- MQTT
- Docker

## 📖 How to Use
### 🔹 Running the Backend (FastAPI Server)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
3. Access the API documentation at `http://localhost:8000/docs`

### 🔹 Running the Frontend (SkySentinel - React)
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React application:
   ```bash
   npm run dev
   ```
4. Open `http://localhost:3000` to access the interface.

## 📡 APIs & Libraries Used
**Backend:** FastAPI, Uvicorn, YOLOv8, OpenCV, TensorFlow, MQTT, SQLAlchemy

**Frontend:** ReactJS, Axios, Tailwind CSS, Three.js

**Mapping & Control:** Pygame, Google Maps API, Mapbox API, Tello SDK (djitellopy)

## 📬 Contact & Contributions
Contributions are welcome! Feel free to submit issues or open a pull request. 🚀
S.Santhosh
U S Aashika vijeta
S.Rishi kumar
S.Yogeshwaran
Prabakar
Surya
Pugazanthi
Jeba Maanyu
