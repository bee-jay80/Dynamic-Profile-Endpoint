from datetime import datetime, timezone
import logging

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets

import os
from dotenv import load_dotenv
load_dotenv()



try:
    import requests
except Exception:  # pragma: no cover - fallback to urllib if requests not installed
    requests = None

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        """Return profile JSON with dynamic UTC timestamp and a cat fact fetched from external API."""
        user = {
            "email": os.getenv("MY_EMAIL"),
            "name": os.getenv("MY_NAME"),
            "stack": "Python/Django",
        }

        # Current UTC timestamp in ISO 8601 format with Z
        timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds')

        # Default fallback fact
        fact = "Could not fetch a cat fact at this time."

        catfact_url = "https://catfact.ninja/fact"
        timeout_seconds = 10

        # Try using requests if available
        try:
            if requests is not None:
                resp = requests.get(catfact_url, timeout=timeout_seconds)
                if resp.status_code == 200:
                    data = resp.json()
                    fact = data.get("fact")
                else:
                    logger.warning("Cat Facts API returned status %s", resp.status_code)
            else:
                # minimal fallback using urllib
                from urllib.request import urlopen
                import json

                with urlopen(catfact_url, timeout=timeout_seconds) as f:
                    data = json.load(f)
                    fact = data.get("fact") or fact
        except Exception as e:
            logger.exception("Failed to fetch cat fact: %s", e)

        return Response({
            "status": "success",
            "user": user,
            "timestamp": timestamp,
            "fact": fact,
        }, status=status.HTTP_200_OK)