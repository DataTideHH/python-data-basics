"""JSON normalization basics.

This example parses an API-like JSON document, reads nested dictionaries and
lists, and converts selected values into a tabular pandas DataFrame.
"""

from __future__ import annotations

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

    frame = pd.DataFrame(rows)

    print("Normalized table:")
    print(frame)


if __name__ == "__main__":
    main()
