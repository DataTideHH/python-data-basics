"""Optional Ollama localhost API example.

The request works only when Ollama is running locally and the configured model
is available. It uses no cloud API key, credentials or tokens.
"""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def main() -> None:
    payload = {
        "model": MODEL,
        "prompt": "Explain JSON in one short sentence.",
        "stream": False,
    }

    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=30) as response:
            raw_body = response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as exc:
        print("Ollama request failed.")
        print("This is expected if Ollama is not running locally or the model is missing.")
        print(f"Details: {exc}")
        return

    data = json.loads(raw_body)

    print("Ollama response:")
    print(data.get("response", "").strip())


if __name__ == "__main__":
    main()
