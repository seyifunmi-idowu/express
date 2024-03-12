from urllib.parse import quote

import requests
from django.conf import settings


class GoogleMapsService:
    SECRET_KEY = settings.GOOGLE_API_KEY
    GOOGLE_SEARCH_LOCATION = settings.GOOGLE_SEARCH_LOCATION
    GOOGLE_SEARCH_RADIUS = settings.GOOGLE_SEARCH_RADIUS
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

    @classmethod
    def search_address(cls, query):
        """ sample_response = {
            "html_attributions": [],
            "next_page_token": "ATplDJagFuVPNguTxS6tYg",
            "results": [
                {
                    "business_status": "OPERATIONAL",
                    "formatted_address": "PG59+2QR, Father Hunter Street, High Level, Asuir 970101, Benue, Nigeria",
                    "geometry": {
                        "location": {"lat": 7.707562899999999, "lng": 8.5194119},
                        "viewport": {
                            "northeast": {
                                "lat": 7.708916729892721,
                                "lng": 8.520754729892721,
                            },
                            "southwest": {
                                "lat": 7.706217070107277,
                                "lng": 8.518055070107277,
                            },
                        },
                    },
                    "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png",
                    "icon_background_color": "#909CE1",
                    "icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet",
                    "name": "Smile View Hotel Extension",
                    "photos": [
                        {
                            "height": 2016,
                            "html_attributions": [
                                '<a href="https://maps.google.com/maps/contrib/106747107223341631050">Desmond Medix</a>'
                            ],
                            "photo_reference": "ATplDJY7PkxXPt7fOtHk4yh1fIDmK22Q",
                            "width": 4032,
                        }
                    ],
                    "place_id": "ChIJu-U-bS-AUBARmZruJiiCoE4",
                    "rating": 3.7,
                    "reference": "ChIJu-U-bS-AUBARmZruJiiCoE4",
                    "types": ["lodging", "point_of_interest", "establishment"],
                    "user_ratings_total": 431,
                },
                {
                    "business_status": "OPERATIONAL",
                    "formatted_address": "PG77+WGG, Township, Makurdi 970101, Benue, Nigeria",
                    "geometry": {
                        "location": {
                            "lat": 7.714796199999999,
                            "lng": 8.513863599999999,
                        },
                        "viewport": {
                            "northeast": {
                                "lat": 7.716119679892721,
                                "lng": 8.515257579892722,
                            },
                            "southwest": {
                                "lat": 7.713420020107277,
                                "lng": 8.512557920107279,
                            },
                        },
                    },
                    "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png",
                    "icon_background_color": "#909CE1",
                    "icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet",
                    "name": "Smile View Hotel Anex",
                    "photos": [
                        {
                            "height": 2560,
                            "html_attributions": [
                                '<a href="https://maps.google.com/maps/contrib/107663795223921656289">Abaver Justine</a>'
                            ],
                            "photo_reference": "ATplDJUxLxFG7uda1r1GfDF",
                            "width": 1920,
                        }
                    ],
                    "place_id": "ChIJ3yw7dDuAUBARDe4S1lKB660",
                    "rating": 3.5,
                    "reference": "ChIJ3yw7dDuAUBARDe4S1lKB660",
                    "types": ["lodging", "point_of_interest", "establishment"],
                    "user_ratings_total": 330,
                },
            ],
            "status": "OK",
        } """
        encoded_address = quote(query)
        url = f"{cls.BASE_URL}/place/textsearch/json?query={encoded_address}&key={cls.SECRET_KEY}&location={cls.GOOGLE_SEARCH_LOCATION}&radius={cls.GOOGLE_SEARCH_RADIUS}"
        response = requests.get(url)
        return response.json()
