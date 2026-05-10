# VENµS Satellite Imagery Search Engine 🛰️

An automated, interactive search engine for locating and downloading VENµS satellite imagery, developed for the Department of Geography and Environmental Development at Ben-Gurion University of the Negev.

## Project Overview
This project simplifies the process of discovering satellite data from the university's large-scale archive. It provides a user-friendly interface to filter metadata based on scientific parameters and download the corresponding products directly to the user's local environment.

## Key Features
* **Dynamic Filtering:** Search by Mission Phase (VM01, VM03, VM05), Processing Levels (L1, L2), and Cloud Percentage.
* **Automated Site Selection:** The "Site ID" (Tile) dropdown updates dynamically based on the selected mission phase.
* **Temporal Constraints:** Calendar date pickers are automatically restricted to the satellite's specific operational periods to prevent empty search results.
* **Direct Download:** Integrated backend mechanism to serve `.DBL` files directly from the university's network storage (**Drive V:**).
* **Interactive Map (In thinking pross):** Visualizing tile locations over Israel using Leaflet.js.

## technology Stack
* **Backend:** Python (FastAPI, Uvicorn)
* **Database:** SQLite
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
* **API Architecture:** RESTful API with STAC-inspired metadata formatting.

##  Getting Started

### Prerequisites
1. An active **BGU VPN** connection.
2. University network storage mapped as **Drive V:** on your local machine.
3. Python environment (Conda recommended).

### Running the Application
1. **Start the Backend:**
   Open your terminal or Git Bash and run:
   ```bash
   python venus_app.py
