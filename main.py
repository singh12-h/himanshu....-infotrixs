import requests
import time

# Global variable to store favorite cities
favorite_cities = []

# Define ANSI color codes
GREEN = "\033[32m"
RED = "\033[31m"
PURPLE = "\033[35m"
BLUE = "\033[34m"
PINK = "\033[95m"
RESET = "\033[0m"


def get_weather(city, api_key):
  base_url = "http://api.weatherapi.com/v1/current.json"
  complete_url = f"{base_url}?key={api_key}&q={city}&aqi=no"
  response = requests.get(complete_url)

  try:
    data = response.json()
    if "error" in data:
      return f"{RED}City not found{RESET}"
  except requests.exceptions.JSONDecodeError:
    return f"{RED}Error: Unable to retrieve weather data. Please check the city name and try again.{RESET}"

  try:
    main = data["current"]
    temperature = main["temp_c"]
    pressure = main["pressure_mb"]
    humidity = main["humidity"]
    weather_desc = main["condition"]["text"]

    return f"{GREEN}Temperature (°C):{RESET} {temperature}\n{PURPLE}Pressure (mb):{RESET} {pressure}\n{BLUE}Humidity (%):{RESET} {humidity}\n{PURPLE}Description:{RESET} {weather_desc}"

  except KeyError:
    return f"{RED}Error: Unable to retrieve weather data. Please check the city name and try again.{RESET}"


# Display the list of favorite cities
def display_favorites():
  print("\nFavorite Cities:")
  for idx, city in enumerate(favorite_cities, start=1):
    print(f"{idx}. {city}")


# Replace 'YOUR_API_KEY' with your WeatherAPI key
api_key = '2eb1cb23325546b58c9174545230110'

while True:
  # Display options for user to choose
  print(f"{GREEN}Options:")
  print(f"1. {PURPLE}Check weather by city")
  print(f"2. {BLUE}Add city to favorites")
  print(f"3. {PURPLE}Remove city from favorites")
  print(f"4. {PURPLE}Display favorite cities")
  print(f"5. {PURPLE}Auto-refresh every 15 seconds")
  print(f"6. {RED}Quit{RESET}")

  choice = input(f"{GREEN}Enter your choice: {RESET}")

  if choice == '1':
    city = input(f"{PINK}Enter city name: {RESET}")
    result = get_weather(city, api_key)

    print(result)

  elif choice == '2':
    city = input(f"{PURPLE}Enter city name to add to favorites: {RESET}")
    favorite_cities.append(city)
    print(f"{city} added to favorites.")

  elif choice == '3':
    display_favorites()
    index = int(
        input(f"{PURPLE}Enter the index of the city to remove: {RESET}"))
    if 1 <= index <= len(favorite_cities):
      removed_city = favorite_cities.pop(index - 1)
      print(f"{removed_city} removed from favorites.")
    else:
      print(f"{RED}Invalid index.{RESET}")

  elif choice == '4':
    display_favorites()

  elif choice == '5':
    refresh_interval = int(
        input(f"{PURPLE}Enter refresh interval in seconds (15-30): {RESET}"))
    if 15 <= refresh_interval <= 30:
      while True:
        for city in favorite_cities:
          result = get_weather(city, api_key)
          print(result)

        time.sleep(refresh_interval)
    else:
      print(f"{RED}Interval should be between 15 and 30 seconds.{RESET}")

  elif choice == '6':
    break
print()
print(f"{GREEN}Goodbye!{RESET}")
