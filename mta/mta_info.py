#! /usr/bin/python3

from google.transit import gtfs_realtime_pb2
from enum import Enum
import requests
import time


class MTAInfo:
    def __init__(self, api_key):
        self.lines = {
            "E": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
            "M": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",
            "R": "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
        }

        self.stops = {
            "G21S": {"name": "Queens Plaza", "lines": ["E", "M", "R"]},
            "D14N": {"name": "7th Ave", "lines": ["E"]},
            "A28N": {"name": "Penn Station", "lines": ["E"]},
        }
        self.api_key = api_key

    def is_stop(self, stop_id):
        return stop_id in self.stops

    def is_line(self, line):
        return line in self.lines

    def get_endpoints(self, stop_id):
        endpoints = []
        for line in self.stops[stop_id]["lines"]:
            endpoints.append(self.lines[line])

        return endpoints

    def get_stop_arrivals(self, stop_id):
        arrivals = []

        feed = gtfs_realtime_pb2.FeedMessage()
        headers = {"x-api-key": self.api_key}
        for endpoint in self.get_endpoints(stop_id=stop_id):
            response = requests.get(
                endpoint,
                headers=headers,
            )
            feed.ParseFromString(response.content)
            for entity in feed.entity:
                if entity.HasField("trip_update"):
                    if self.is_line(entity.trip_update.trip.route_id):
                        for update in entity.trip_update.stop_time_update:
                            if self.is_stop(stop_id=update.stop_id):
                                now = time.time()
                                until_arrival = update.arrival.time - now
                                arrivals.append(
                                    {
                                        "line": entity.trip_update.trip.route_id,
                                        "time": round(until_arrival / 60),
                                    }
                                )

        arrivals.sort(key=lambda x: x["time"])
        return {"stop": stop_id, "arrivals": arrivals}
