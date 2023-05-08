import csv
import requests

def update_coordinates(input_file, output_file, api_key):
    def get_coordinates(location_name, retries=3):
        if location_name in location_cache:
            return location_cache[location_name]

        for attempt in range(retries):
            try:
                base_url = "https://maps.googleapis.com/maps/api/geocode/json"
                params = {
                    "address": f"{location_name}, Karnataka, India",
                    "key": api_key
                }
                response = requests.get(base_url, params=params)
                data = response.json()

                if data["status"] == "OK":
                    location = data["results"][0]["geometry"]["location"]
                    location_cache[location_name] = (location["lat"], location["lng"])
                    return location["lat"], location["lng"]
                else:
                    print(f"Error fetching coordinates for {location_name}: {data['status']}")
                    return None, None
            except requests.exceptions.RequestException as e:
                print(f"Request error for {location_name}: {e}")
                if attempt == retries - 1:
                    print(f"Failed to fetch coordinates for {location_name} after {retries} retries.")
                    return None, None


    location_cache = {}

    with open(input_file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)

        with open(output_file, "w", newline='') as updated_csv_file:
            csv_writer = csv.writer(updated_csv_file)
            csv_writer.writerow(headers)

            for row in csv_reader:
                if float(row[5]) != 0 and float(row[6]) != 0:
                    # Skip rows with non-zero latitude and longitude
                    csv_writer.writerow(row)
                    continue

                location_name = row[4].strip('"')  # Remove double quotes
                lat, lng = get_coordinates(location_name)
                if lat and lng:
                    row[5] = lat
                    row[6] = lng

                csv_writer.writerow(row)

if __name__ == "__main__":
    input_file = "input.csv"
    output_file = "output.csv"
    api_key = ""  # Replace with your actual API key
    update_coordinates(input_file, output_file, api_key)
    print("Coordinates updated successfully.")
