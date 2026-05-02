import polyline
import math


MAX_RANGE_MILES = 500
MPG = 10


def decode_route_geometry(encoded_geometry):

    coordinates = polyline.decode(
        encoded_geometry
    )

    return coordinates


# Faster distance approximation
def fast_distance_miles(
    lat1,
    lon1,
    lat2,
    lon2
):

    return math.sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    ) * 69


def find_nearby_stations(
    route_geometry,
    stations_df
):

    nearby_stations = []

    route_coordinates = decode_route_geometry(
        route_geometry
    )

    # Extract route latitude/longitude
    route_lats = [
        point[0]
        for point in route_coordinates
    ]

    route_lons = [
        point[1]
        for point in route_coordinates
    ]

    # Bounding box filtering
    min_lat = min(route_lats) - 1
    max_lat = max(route_lats) + 1

    min_lon = min(route_lons) - 1
    max_lon = max(route_lons) + 1

    filtered_stations = stations_df[
        (stations_df["latitude"] >= min_lat) &
        (stations_df["latitude"] <= max_lat) &
        (stations_df["longitude"] >= min_lon) &
        (stations_df["longitude"] <= max_lon)
    ]

    # Check only filtered stations
    for _, station in filtered_stations.iterrows():

        station_lat = station["latitude"]
        station_lon = station["longitude"]

        # Larger route sampling for speed
        for point in route_coordinates[::150]:

            route_lat = point[0]
            route_lon = point[1]

            distance = fast_distance_miles(
                station_lat,
                station_lon,
                route_lat,
                route_lon
            )

            # Nearby station threshold
            if distance <= 20:

                nearby_stations.append({

                    "truckstop_name": station["Truckstop Name"],

                    "city": station["City"],

                    "state": station["State"],

                    "price": round(
                        float(station["Retail Price"]),
                        2
                    ),

                    "latitude": station_lat,

                    "longitude": station_lon,

                    "distance_from_route_miles": round(
                        distance,
                        2
                    )
                })

                break

    return nearby_stations


def select_cheapest_stops(
    stations,
    fuel_stops_required
):

    sorted_stations = sorted(
        stations,
        key=lambda x: x["price"]
    )

    if fuel_stops_required == 0:

        return []

    return sorted_stations[
        :fuel_stops_required
    ]


def calculate_total_cost(
    distance_miles,
    avg_price
):

    gallons_needed = (
        distance_miles / MPG
    )

    total_cost = (
        gallons_needed * avg_price
    )

    return round(total_cost, 2)


def calculate_fuel_stops_required(
    distance_miles
):

    return max(
        0,
        math.ceil(
            distance_miles / MAX_RANGE_MILES
        ) - 1
    )