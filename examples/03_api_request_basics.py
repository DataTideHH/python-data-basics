"""
Basic public API request example.

This example calls the Open-Meteo API for Hamburg.
It uses only Python standard-library modules for the HTTP request.

No API key is required.
No credentials or tokens are used.
"""

import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=53.5503"
    "&longitude=10.0007"
    "&current=temperature_2m,precipitation,cloud_cover,wind_speed_10m"
)


def main() -> None:
    try:
        with urlopen(OPEN_METEO_URL, timeout=15) as response:
            raw_body = response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"API request failed: {exc}")
        return

    data = json.loads(raw_body)

    print("Top-level JSON keys:")
    print(list(data.keys()))

    print("\nCurrent weather values:")
    current = data.get("current", {})
    for key, value in current.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
