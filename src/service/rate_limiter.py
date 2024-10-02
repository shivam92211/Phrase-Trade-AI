from fastapi import Request, HTTPException
from time import time


class IPRateLimiter:
    def __init__(self, rate_limit: int, minutes: int):
        self.rate_limit = rate_limit
        self.time_window = minutes * 60  # Convert minutes to seconds
        self.request_counts = {}  # Dictionary to store {ip: [timestamps]}
        self.clean_on_count = 100  # Optional: clean up after this many entries

    def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        current_time = time()

        # Initialize if the IP is new
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []

        # Clean up old timestamps outside the time window
        self.request_counts[client_ip] = [
            t
            for t in self.request_counts[client_ip]
            if current_time - t < self.time_window
        ]

        # Check if IP exceeds the rate limit
        if len(self.request_counts[client_ip]) >= self.rate_limit:
            raise HTTPException(status_code=429, detail="Too many requests")

        # Record the new request timestamp
        self.request_counts[client_ip].append(current_time)

        # Optionally clean up IPs if the dictionary grows too large
        if len(self.request_counts) > self.clean_on_count:
            self._clean_up()

    def _clean_up(self):
        # Remove IPs with no recent requests to prevent memory growth
        self.request_counts = {
            ip: timestamps
            for ip, timestamps in self.request_counts.items()
            if timestamps
        }
