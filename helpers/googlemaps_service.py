from urllib.parse import quote

import requests
from django.conf import settings


class GoogleMapsService:
    SECRET_KEY = settings.GOOGLE_API_KEY
    BASE_URL = "https://maps.googleapis.com/maps/api"

    @classmethod
    def get_address_details(cls, address: str) -> dict:
        """ sample_response = {
            "results": [
                {
                    "address_components": [
                        {
                            "long_name": "24",
                            "short_name": "24",
                            "types": ["street_number"],
                        },
                        {
                            "long_name": "olorunkemi Street",
                            "short_name": "Olorunkemi Street",
                            "types": ["route"],
                        },
                        {
                            "long_name": "Bariga",
                            "short_name": "Bariga",
                            "types": ["neighborhood", "political"],
                        },
                        {
                            "long_name": "Lagos",
                            "short_name": "Lagos",
                            "types": ["locality", "political"],
                        },
                        {
                            "long_name": "Lad-Lak/Bariga",
                            "short_name": "Lad-Lak/Bariga",
                            "types": ["administrative_area_level_3", "political"],
                        },
                        {
                            "long_name": "Shomolu",
                            "short_name": "Shomolu",
                            "types": ["administrative_area_level_2", "political"],
                        },
                        {
                            "long_name": "Lagos",
                            "short_name": "LA",
                            "types": ["administrative_area_level_1", "political"],
                        },
                        {
                            "long_name": "Nigeria",
                            "short_name": "NG",
                            "types": ["country", "political"],
                        },
                        {
                            "long_name": "102216",
                            "short_name": "102216",
                            "types": ["postal_code"],
                        },
                    ],
                    "formatted_address": "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria",
                    "geometry": {
                        "location": {"lat": 6.5358762, "lng": 3.3829932},
                        "location_type": "ROOFTOP",
                        "viewport": {
                            "northeast": {
                                "lat": 6.537225380291502,
                                "lng": 3.384342230291502,
                            },
                            "southwest": {
                                "lat": 6.534527419708497,
                                "lng": 3.381644269708498,
                            },
                        },
                    },
                    "place_id": "ChIJw8aHvQiNOxAR3u3AuqXWmCs",
                    "plus_code": {
                        "compound_code": "G9PM+95 Lagos, Nigeria",
                        "global_code": "6FR5G9PM+95",
                    },
                    "types": ["street_address"],
                }
            ],
            "status": "OK",
        } """
        encoded_address = quote(address)
        url = f"{cls.BASE_URL}/geocode/json?address={encoded_address}&key={cls.SECRET_KEY}"
        response = requests.get(url)
        return response.json()

    @classmethod
    def get_latitude_and_longitude_details(cls, latitude, longitude):
        """ sample_response = {
            "plus_code": {
                "compound_code": "G9PM+955 Lagos, Nigeria",
                "global_code": "6FR5G9PM+955",
            },
            "results": [
                {
                    "address_components": [
                        {
                            "long_name": "24",
                            "short_name": "24",
                            "types": ["street_number"],
                        },
                        {
                            "long_name": "olorunkemi Street",
                            "short_name": "Olorunkemi Street",
                            "types": ["route"],
                        },
                        {
                            "long_name": "Bariga",
                            "short_name": "Bariga",
                            "types": ["neighborhood", "political"],
                        },
                        {
                            "long_name": "Lagos",
                            "short_name": "Lagos",
                            "types": ["locality", "political"],
                        },
                        {
                            "long_name": "Lad-Lak/Bariga",
                            "short_name": "Lad-Lak/Bariga",
                            "types": ["administrative_area_level_3", "political"],
                        },
                        {
                            "long_name": "Shomolu",
                            "short_name": "Shomolu",
                            "types": ["administrative_area_level_2", "political"],
                        },
                        {
                            "long_name": "Lagos",
                            "short_name": "LA",
                            "types": ["administrative_area_level_1", "political"],
                        },
                        {
                            "long_name": "Nigeria",
                            "short_name": "NG",
                            "types": ["country", "political"],
                        },
                        {
                            "long_name": "102216",
                            "short_name": "102216",
                            "types": ["postal_code"],
                        },
                    ],
                    "formatted_address": "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria",
                    "geometry": {
                        "location": {"lat": 6.5358762, "lng": 3.3829932},
                        "location_type": "ROOFTOP",
                        "viewport": {
                            "northeast": {
                                "lat": 6.537225180291502,
                                "lng": 3.384342180291502,
                            },
                            "southwest": {
                                "lat": 6.534527219708497,
                                "lng": 3.381644219708498,
                            },
                        },
                    },
                    "place_id": "ChIJw8aHvQiNOxAR3u3AuqXWmCs",
                    "plus_code": {
                        "compound_code": "G9PM+95 Lagos, Nigeria",
                        "global_code": "6FR5G9PM+95",
                    },
                    "types": ["street_address"],
                },
                {
                    "address_components": [
                        {
                            "long_name": "24",
                            "short_name": "24",
                            "types": ["street_number"],
                        },
                        {
                            "long_name": "olorunkemi Street",
                            "short_name": "Olorunkemi Street",
                            "types": ["route"],
                        },
                        {
                            "long_name": "Bariga",
                            "short_name": "Bariga",
                            "types": [
                                "political",
                                "sublocality",
                                "sublocality_level_1",
                            ],
                        },
                        {
                            "long_name": "Lagos",
                            "short_name": "Lagos",
                            "types": ["locality", "political"],
                        },
                        {
                            "long_name": "Lad-Lak/Bariga",
                            "short_name": "Lad-Lak/Bariga",
                            "types": ["administrative_area_level_3", "political"],
                        },
                        {
                            "long_name": "Shomolu",
                            "short_name": "Shomolu",
                            "types": ["administrative_area_level_2", "political"],
                        },
                        {
                            "long_name": "Lagos",
                            "short_name": "LA",
                            "types": ["administrative_area_level_1", "political"],
                        },
                        {
                            "long_name": "Nigeria",
                            "short_name": "NG",
                            "types": ["country", "political"],
                        },
                        {
                            "long_name": "102216",
                            "short_name": "102216",
                            "types": ["postal_code"],
                        },
                    ],
                    "formatted_address": "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria",
                    "geometry": {
                        "location": {"lat": 6.535848199999999, "lng": 3.3829791},
                        "location_type": "RANGE_INTERPOLATED",
                        "viewport": {
                            "northeast": {
                                "lat": 6.537197180291502,
                                "lng": 3.384328080291502,
                            },
                            "southwest": {
                                "lat": 6.534499219708497,
                                "lng": 3.381630119708498,
                            },
                        },
                    },
                    "place_id": "EiwyNCBPbG9ydW5rZW1pIFN0cmVldCwgQmFyaWdhLCBMYWdvcywgTmlnZXJpYSIaEhgKFAoSCXkA3rwIjTsQEaJKttTzxxoqEBg",
                    "types": ["street_address"],
                },
                {
                    "address_components": [
                        {
                            "long_name": "Nigeria",
                            "short_name": "NG",
                            "types": ["country", "political"],
                        }
                    ],
                    "formatted_address": "Nigeria",
                    "geometry": {
                        "bounds": {
                            "northeast": {"lat": 13.8856449, "lng": 14.677982},
                            "southwest": {"lat": 4.1821001, "lng": 2.676932},
                        },
                        "location": {"lat": 9.081999, "lng": 8.675277},
                        "location_type": "APPROXIMATE",
                        "viewport": {
                            "northeast": {"lat": 13.8856449, "lng": 14.677982},
                            "southwest": {"lat": 4.1821001, "lng": 2.676932},
                        },
                    },
                    "place_id": "ChIJDY2kfa8LThARyAvFaEH-qJk",
                    "types": ["country", "political"],
                },
            ],
            "status": "OK",
        } """
        url = f"{cls.BASE_URL}/geocode/json?latlng={latitude},{longitude}&key={cls.SECRET_KEY}"
        response = requests.get(url)
        return response.json()

    @classmethod
    def get_distance_matrix(cls, origin_latlng, destination_latlng, mode="driving"):
        """ sample_response = {
            "destination_addresses": [
                "67 Oduduwa Way, Ikeja GRA, Ikeja 101233, Lagos, Nigeria"
            ],
            "origin_addresses": [
                "24 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria"
            ],
            "rows": [
                {
                    "elements": [
                        {
                            "distance": {"text": "7.8 km", "value": 7816},
                            "duration": {"text": "22 mins", "value": 1307},
                            "duration_in_traffic": {"text": "19 mins", "value": 1147},
                            "status": "OK",
                        }
                    ]
                }
            ],
            "status": "OK",
        } """

        url = f"{cls.BASE_URL}/distancematrix/json?origins={origin_latlng}&destinations={destination_latlng}&mode={mode}&key={cls.SECRET_KEY}"
        response = requests.get(url)
        return response.json()
