"""
JSON basics.

This example demonstrates:
- parsing JSON text
- accessing nested dictionaries and lists
- converting selected values into a pandas DataFrame

The structure is similar to many API responses.
"""

import json

import pandas as pd


JSON_TEXT = """
{
  "source": "example-api",
  "generated_at": "2026-06-15T10:00:00Z",
  "cities": [
    {
      "name": "Hamburg",
      "country": "DE",
      "metrics": {
        "temperature_c": 18.5,
        "cloud_cover_percent": 70
      }
    },
    {
      "name": "Berlin",
      "country": "DE",
      "metrics": {
        "temperature_c": 21.2,
        "cloud_cover_percent": 45
      }
    }
  ]
}
"""


def main() -> None:
    data = json.loads(JSON_TEXT)

    rows = []
    for city in data["cities"]:
        rows.append(
            {
                "name": city["name"],
                "country": city["country"],
                "temperature_c": city["metrics"]["temperature_c"],
                "cloud_cover_percent": city["metrics"]["cloud_cover_percent"],
                "source": data["source"],
                "generated_at": data["generated_at"],
            }
        )

    df = pd.DataFrame(rows)

    print("Normalized table:")
    print(df)


if __name__ == "__main__":
    main()
