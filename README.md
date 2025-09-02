
# Trip Planner App

## Purpose
Trip Planner is a full-stack application built with Django (backend) and React (frontend) to help property-carrying drivers plan trips, visualize routes, and generate FMCSA-compliant ELD log sheets. The app automates trip planning, route mapping, and log generation for regulatory compliance and operational efficiency.

## Features
- **Trip Planning:** Enter current location, pickup, dropoff, and cycle hours used to plan a trip.
- **Route Visualization:** Displays the route on a map, including stops and rest breaks (integrated with a free map API).
- **Automatic ELD Log Generation:** Splits trips into daily logs and generates compliant duty events for each day, including driving, off-duty, sleeper berth, on-duty, fuel stops, and rest breaks.
- **Multi-day Support:** Handles trips spanning multiple days, creating separate log sheets for each day.
- **FMCSA Compliance:** Follows 70hrs/8days HOS rules, includes fueling at least every 1,000 miles, and 1 hour for pickup/drop-off.
- **Modern UI/UX:** React frontend for a clean, user-friendly experience.

## Technologies
- Django & Django REST Framework (backend API)
- React (frontend)
- OpenStreetMap/OSRM (free map API integration)
- SQLite/Postgres (database)

## How It Works
1. **Create a Trip:** Input trip details (current location, pickup, dropoff, cycle hours used).
2. **Geocoding & Routing:** Backend geocodes locations and calculates route, stops, and rests.
3. **Log Generation:** Backend automatically creates daily logs and duty events for each day of the trip.
4. **Frontend Visualization:** View route map and log sheets in the React app.

## Deployment
- Backend can be hosted on Render.com (see instructions in this repo).
- Frontend can be hosted on Vercel, Netlify, or Render Static Site.

## Getting Started
1. Clone the repo: `git clone <your-repo-url>`
2. Install backend dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start backend: `python manage.py runserver`
5. Install frontend dependencies and start React app (see frontend README).

## API Endpoints
- `/api/v1/trips/` - Create and manage trips
- `/api/v1/logs/compliant_log/` - Get FMCSA-compliant log sheet for a trip and date

## Assessment Requirements
- Live hosted version (Render, Vercel, etc.)
- Loom video walkthrough
- Github code sharing
- Good design and aesthetics

## License
MIT
