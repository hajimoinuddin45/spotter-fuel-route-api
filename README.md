# Spotter Fuel Route Optimization API

## Overview

This project is a Django REST API that calculates optimal fuel stops along a driving route in the United States.

The API:

* Accepts a start and destination location
* Uses OpenRouteService for route calculation
* Identifies nearby fuel stations along the route
* Selects cost-effective fuel stops based on fuel prices
* Calculates estimated total fuel cost
* Supports multiple fuel stops based on vehicle range constraints
* Minimizes external API calls for performance

The project was built as part of a Backend Django Engineer technical assessment.

---

# Features

## Route Optimization

* Calculates route distance and duration
* Uses only one routing API call per request
* Returns encoded route geometry

## Fuel Stop Recommendation

* Finds fuel stations near the route corridor
* Filters stations using geospatial distance calculations
* Selects cheapest nearby stations
* Supports multiple fuel stops for long trips

## Fuel Cost Estimation

Assumptions:

* Vehicle range = 500 miles
* Vehicle MPG = 10

Formula:

Fuel Cost = (Distance / MPG) × Average Fuel Price

---

# Tech Stack

* Python 3.12
* Django 6
* Django REST Framework
* OpenRouteService API
* Geopy
* Polyline
* Pandas

---

# Project Structure

```text
spotter-fuel-route-api/
│
├── api/
│   ├── services/
│   │   ├── optimization_service.py
│   │   ├── routing_service.py
│   │   └── station_service.py
│   │
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── scripts/
│   └── geocode_fuel_stations.py
│
├── fuel-stations-geocoded.csv
├── requirements.txt
├── manage.py
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/hajimoinuddin45/spotter-fuel-route-api.git
```

```bash
cd spotter-fuel-route-api
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
ORS_API_KEY=your_openrouteservice_api_key
```

---

## 5. Get OpenRouteService API Key

1. Visit:

[https://openrouteservice.org/dev/#/signup](https://openrouteservice.org/dev/#/signup)

2. Create an account

3. Generate an API key

4. Add the key to your `.env` file

---

## 6. Run Migrations

```bash
python manage.py migrate
```

---

## 7. Start Development Server

```bash
python manage.py runserver
```

Server:

```text
http://127.0.0.1:8000/
```

---

# API Usage

## Endpoint

```text
POST /api/optimize-route/
```

Full URL:

```text
http://127.0.0.1:8000/api/optimize-route/
```

---

# Request Example

## Request Body

```json
{
    "start": "Los Angeles, CA",
    "end": "Chicago, IL"
}
```

---

# Example Response

```json
{
    "start": "Los Angeles, CA",
    "end": "Chicago, IL",
    "distance_miles": 2015.49,
    "duration_hours": 31.56,
    "fuel_stops_found": 123,
    "recommended_fuel_stops": [
        {
            "truckstop_name": "Henderson Fuel Mart",
            "city": "Henderson",
            "state": "NE",
            "price": 2.9,
            "latitude": 40.7810033,
            "longitude": -97.8123127,
            "distance_from_route_miles": 2.85
        }
    ],
    "average_fuel_price": 2.96,
    "estimated_total_fuel_cost": 596.59,
    "fuel_stops_required": 4
}
```

---

# How the Optimization Works

## Step 1 — Route Calculation

The API sends one request to OpenRouteService to:

* calculate route
* calculate distance
* calculate duration
* retrieve encoded route geometry

---

## Step 2 — Route Geometry Decoding

The encoded polyline route is decoded into geographic coordinates using the `polyline` package.

---

## Step 3 — Bounding Box Optimization

To improve performance:

* route latitude/longitude bounds are calculated
* only stations inside the route region are evaluated

This significantly reduces expensive geodesic calculations.

---

## Step 4 — Nearby Station Detection

The API:

* samples route points
* calculates geodesic distance
* identifies stations within 20 miles of the route

---

## Step 5 — Cheapest Fuel Selection

Nearby stations are sorted by fuel price.

The API returns the cheapest stations based on:

* route distance
* required fuel stops
* vehicle range

---

## Step 6 — Fuel Cost Calculation

Fuel cost is estimated using:

```text
Fuel Cost = (Distance Miles / MPG) × Fuel Price
```

Vehicle assumptions:

* MPG = 10
* Max Range = 500 miles

---

# Performance Optimizations

The API was optimized to reduce latency:

* Only one routing API call per request
* Fuel station coordinates are preprocessed and cached locally
* Bounding-box filtering reduces unnecessary station calculations
* Route point sampling reduces geodesic computation load

---

# Fuel Dataset Preprocessing

Fuel station addresses were geocoded beforehand using a preprocessing script.

Script:

```text
scripts/geocode_fuel_stations.py
```

This avoids repeated geocoding during API requests.

---

# Error Handling

The API handles:

* invalid locations
* missing request fields
* routing API failures
* excessive route distances
* unavailable station matches

---

# Example Test Routes

## Short Route

```json
{
    "start": "Austin, TX",
    "end": "Houston, TX"
}
```

## Medium Route

```json
{
    "start": "Dallas, TX",
    "end": "Chicago, IL"
}
```

## Long Route

```json
{
    "start": "Los Angeles, CA",
    "end": "Chicago, IL"
}
```

## East Coast Route

```json
{
    "start": "New York, NY",
    "end": "Miami, FL"
}
```

---

# Future Improvements

Potential enhancements include:

* stage-aware fuel stop distribution
* Redis caching
* asynchronous processing
* frontend map visualization
* route visualization with Leaflet or Mapbox
* PostgreSQL/PostGIS integration
* advanced path optimization algorithms

---

# Author

Haji Moinuddin

GitHub:

[https://github.com/hajimoinuddin45](https://github.com/hajimoinuddin45)
