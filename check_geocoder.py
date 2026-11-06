#!/usr/bin/env python3
"""Check public Nominatim responses with a small, sequential request batch."""

import json
import time
import urllib.error
import urllib.parse
import urllib.request


def main():
    query = urllib.parse.urlencode({
        "lat": 55.7558,
        "lon": 37.6173,
        "format": "jsonv2",
        "accept-language": "ru",
    })
    url = f"https://nominatim.openstreetmap.org/reverse?{query}"
    for number in range(1, 6):
        request = urllib.request.Request(
            url, headers={"User-Agent": "NominatimCheck/1.0 (https://github.com/frol86/nominatim)"}
        )
        started = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                data = json.load(response)
                print(f"{number}: HTTP {response.status}, {time.monotonic() - started:.2f}s", flush=True)
                print(data.get("display_name", data), flush=True)
        except urllib.error.HTTPError as error:
            print(f"{number}: HTTP {error.code}; Retry-After: {error.headers.get('Retry-After', '-')}", flush=True)
            if error.code in (403, 429):
                return 1
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            print(f"Request failed: {error}", flush=True)
            return 1
        if number < 5:
            time.sleep(1.1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
