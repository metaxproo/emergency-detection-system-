#  EDS | Emergency Detection System

A sophisticated, real-time monitoring and management dashboard designed for security and emergency response. This interface serves as the central hub for an AI-powered Smart Home Command Center, integrating live data feeds with geospatial mapping.

---

##  Project Overview
The **EDS Master Command Center** is the frontend component of a comprehensive emergency response ecosystem. It is designed to bridge the gap between AI-driven incident detection (such as YOLO object detection) and human-led authority dispatch.

The **Police/Hospital/Firestation Center** is the receiving component of the response to take suitable action for the  incident. 

The system monitors for specific high-risk incidents—including **Weapon Detection**, **Fire Hazards**, and **Medical Emergencies (Falls)**—by communicating with a remote AI server (FastAPI). It visualizes these threats on an interactive map, allowing for immediate situational awareness and rapid coordination with emergency services.

---

##  Tech Stack
* **Frontend:** HTML5, CSS3 (Custom Metallic/Cyberpunk UI).
* **Interactivity:** JavaScript (Asynchronous Fetch API & DOM Manipulation).
* **Mapping:** Leaflet.js with customized dark-mode tile filters.
* **Backend Integration:** FastAPI (hosted on Google Colab) tunneled via **ngrok**.
* **Data Management:** Integration with Google Sheets and LocalStorage for logging.
* **Typography:** Google Fonts (Orbitron) for a high-tech aesthetic.

---

##  Key Features
* **Real-time Incident Streaming:** Automatically polls the backend every 3 seconds to fetch the latest detected incidents.
* **Interactive Tactical Map:** Displays the exact location of threats with automated panning and marker updates.
* **Manual Location Override:** Allows operators to manually update coordinates by clicking directly on the map.
* **Authority Dispatch System:** One-click triggers to send alerts to Police, Medical, or Fire departments with full event payloads.
* **Live Activity Log:** A chronological record of all system updates and dispatch actions for post-incident reporting.

---

##  Backend Communication & Data Schema
The dashboard communicates with a **FastAPI** server using the following JSON structure for incident reporting:

```json
{
    "id": 4.0,
    "type": "weapon",
    "lat": 30.0444,
    "lng": 31.2357,
    "source": "dashboard_manual",
    "confidence": 1.0,
    "timestamp": "2026-04-15 23:50:00"
}

```
##  Installation & Setup
 1. **Clone the Repository:**
   ```bash
   git clone [(https://metaxproo.github.io/emergency-detection-system-/ ana 3arfa eno msh mazot bas khleh hena)]
   
   ```
 2. **Configure the Endpoint:**
   * Open tryhard.html.
   * Locate the fetch URLs.
   * Replace the ngrok link with your active server URL.
 3. **Launch:**
   * Open tryhard.html in any modern web browser.
     
## 👥 Contributors
This project was developed by:
 * **Jannatallah Mohamed** - *Engineering Student & Full-stack Developer & AI Developer* - https://github.com/metaxproo
 * **Jana Hazem** - *Engineering Student & AI Developer & Full-stack Developer* - https://github.com/janahazem890-lgtm
 * **Ola Abdelnabi** - *Engineering Student & AI Developer & Full-stack Developer*  -https://github.com/olaabdelnabi
 * **Arwa Mohamed** - *Engineering Student & AI Developer & Full-stack Developer* -https://github.com/arwa63/arwa63
##  About the Project
Developed as part of an engineering curriculum focusing on the integration of AI computer vision alerts with functional, user-centric web interfaces.
```

