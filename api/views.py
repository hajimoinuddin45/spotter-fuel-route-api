from rest_framework.decorators import api_view
from rest_framework.response import Response

from geopy.geocoders import Nominatim

from api.services.routing_service import get_route
from api.services.station_service import load_stations

from api.services.optimization_service import (
    find_nearby_stations,
    select_cheapest_stops,
    calculate_total_cost,
    calculate_fuel_stops_required
)


@api_view(["POST"])
def optimize_route(request):

    start = request.data.get("start")
    end = request.data.get("end")

    # Validate request
    if not start or not end:

        return Response({
            "error": "Start and end locations are required"
        }, status=400)

    geolocator = Nominatim(
        user_agent="fuel_optimizer"
    )

    # Geocode locations
    start_location = geolocator.geocode(start)
    end_location = geolocator.geocode(end)

    if not start_location or not end_location:

        return Response({
            "error": "Invalid locations"
        }, status=400)

    # ORS requires [longitude, latitude]
    start_coords = [
        start_location.longitude,
        start_location.latitude
    ]

    end_coords = [
        end_location.longitude,
        end_location.latitude
    ]

    # Fetch route
    route_data = get_route(
        start_coords,
        end_coords
    )

    # Handle ORS API errors
    if "routes" not in route_data:

        return Response({
            "error": "Failed to fetch route",
            "details": route_data
        }, status=500)

    route = route_data["routes"][0]

    summary = route["summary"]

    distance_meters = summary["distance"]

    duration_seconds = summary["duration"]

    # Convert units
    distance_miles = round(
        distance_meters * 0.000621371,
        2
    )

    duration_hours = round(
        duration_seconds / 3600,
        2
    )

    # Encoded polyline geometry
    route_geometry = route["geometry"]

    # Load geocoded stations
    stations_df = load_stations()

    # Find stations near route
    nearby_stations = find_nearby_stations(
        route_geometry,
        stations_df
    )

    # Cheapest nearby stations
    fuel_stops_required = calculate_fuel_stops_required(
        distance_miles
    )

    cheapest_stations = select_cheapest_stops(
        nearby_stations,
        fuel_stops_required
    )

    # Fallback fuel price
    avg_price = 3.50

    if cheapest_stations:

        avg_price = round(
            sum(
                station["price"]
                for station in cheapest_stations
            ) / len(cheapest_stations),
            2
        )

    # Calculate estimated total fuel cost
    total_cost = calculate_total_cost(
        distance_miles,
        avg_price
    )

    return Response({

        "start": start,

        "end": end,

        "distance_miles": distance_miles,

        "duration_hours": duration_hours,

        "fuel_stops_found": len(
            nearby_stations
        ),

        "recommended_fuel_stops": cheapest_stations,

        "average_fuel_price": avg_price,

        "estimated_total_fuel_cost": total_cost,

        "route_geometry_preview": route_geometry[:120],

        "fuel_stops_required": fuel_stops_required
    })