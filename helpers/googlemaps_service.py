from urllib.parse import quote

import requests
from django.conf import settings


class GoogleMapsService:
    SECRET_KEY = settings.GOOGLE_API_KEY
    BASE_URL = "https://maps.googleapis.com/maps/api"

    @classmethod
    def get_address_details(cls, address: str) -> dict:
        encoded_address = quote(address)
        url = f"{cls.BASE_URL}/geocode/json?address={encoded_address}&key={cls.SECRET_KEY}"
        sample_response = {
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
        }
        if sample_response:
            return sample_response
        response = requests.get(url)
        return response.json()

    @classmethod
    def get_latitude_and_longitude_details(cls, latitude, longitude):
        url = f"{cls.BASE_URL}/geocode/json?latlng={latitude},{longitude}&key={cls.SECRET_KEY}"
        sample_response = {
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
                            "long_name": "19",
                            "short_name": "19",
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
                    "formatted_address": "19 Olorunkemi Street, Bariga, Lagos 102216, Lagos, Nigeria",
                    "geometry": {
                        "location": {"lat": 6.535760199999999, "lng": 3.3828315},
                        "location_type": "ROOFTOP",
                        "viewport": {
                            "northeast": {
                                "lat": 6.537109180291502,
                                "lng": 3.384180480291502,
                            },
                            "southwest": {
                                "lat": 6.534411219708497,
                                "lng": 3.381482519708498,
                            },
                        },
                    },
                    "place_id": "ChIJvw4M1zKNOxARHIMSyQipdDc",
                    "plus_code": {
                        "compound_code": "G9PM+84 Lagos, Nigeria",
                        "global_code": "6FR5G9PM+84",
                    },
                    "types": [
                        "clothing_store",
                        "establishment",
                        "point_of_interest",
                        "store",
                    ],
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
                        "bounds": {
                            "northeast": {"lat": 6.5359265, "lng": 3.3834993},
                            "southwest": {"lat": 6.535583, "lng": 3.3828265},
                        },
                        "location": {"lat": 6.5357566, "lng": 3.3831639},
                        "location_type": "GEOMETRIC_CENTER",
                        "viewport": {
                            "northeast": {
                                "lat": 6.537103730291502,
                                "lng": 3.384511880291502,
                            },
                            "southwest": {
                                "lat": 6.534405769708497,
                                "lng": 3.381813919708498,
                            },
                        },
                    },
                    "place_id": "ChIJeQDevAiNOxARokq21PPHGio",
                    "types": ["route"],
                },
                {
                    "address_components": [
                        {
                            "long_name": "G9PM+95",
                            "short_name": "G9PM+95",
                            "types": ["plus_code"],
                        },
                        {
                            "long_name": "Lagos",
                            "short_name": "Lagos",
                            "types": ["locality", "political"],
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
                    ],
                    "formatted_address": "G9PM+95 Lagos, Nigeria",
                    "geometry": {
                        "bounds": {
                            "northeast": {"lat": 6.536, "lng": 3.383},
                            "southwest": {"lat": 6.535875, "lng": 3.382875},
                        },
                        "location": {"lat": 6.5358762, "lng": 3.3829932},
                        "location_type": "GEOMETRIC_CENTER",
                        "viewport": {
                            "northeast": {
                                "lat": 6.537286480291502,
                                "lng": 3.384286480291502,
                            },
                            "southwest": {
                                "lat": 6.534588519708498,
                                "lng": 3.381588519708498,
                            },
                        },
                    },
                    "place_id": "GhIJq9EGu7wkGkARHbkkvV4QC0A",
                    "plus_code": {
                        "compound_code": "G9PM+95 Lagos, Nigeria",
                        "global_code": "6FR5G9PM+95",
                    },
                    "types": ["plus_code"],
                },
                {
                    "address_components": [
                        {
                            "long_name": "Lad-Lak/Bariga",
                            "short_name": "Lad-Lak/Bariga",
                            "types": ["administrative_area_level_3", "political"],
                        },
                        {
                            "long_name": "Somolu",
                            "short_name": "Somolu",
                            "types": [
                                "political",
                                "sublocality",
                                "sublocality_level_1",
                            ],
                        },
                        {
                            "long_name": "Ikeja",
                            "short_name": "Ikeja",
                            "types": ["locality", "political"],
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
                    "formatted_address": "Somolu, Lad-Lak/Bariga 102216, Lagos, Nigeria",
                    "geometry": {
                        "bounds": {
                            "northeast": {"lat": 6.546971699999999, "lng": 3.3904859},
                            "southwest": {"lat": 6.531760999999999, "lng": 3.379643},
                        },
                        "location": {"lat": 6.5376449, "lng": 3.3867683},
                        "location_type": "APPROXIMATE",
                        "viewport": {
                            "northeast": {"lat": 6.546971699999999, "lng": 3.3904859},
                            "southwest": {"lat": 6.531760999999999, "lng": 3.379643},
                        },
                    },
                    "place_id": "ChIJTzPOuw6NOxARsOj-9A79TBU",
                    "types": ["administrative_area_level_3", "political"],
                },
                {
                    "address_components": [
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
                            "long_name": "Oworonshoki",
                            "short_name": "Oworonshoki",
                            "types": ["locality", "political"],
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
                    "formatted_address": "Bariga, Oworonshoki 102216, Lagos, Nigeria",
                    "geometry": {
                        "bounds": {
                            "northeast": {"lat": 6.5479707, "lng": 3.3996527},
                            "southwest": {"lat": 6.5306541, "lng": 3.373531},
                        },
                        "location": {"lat": 6.5391037, "lng": 3.3849441},
                        "location_type": "APPROXIMATE",
                        "viewport": {
                            "northeast": {"lat": 6.5479707, "lng": 3.3996527},
                            "southwest": {"lat": 6.5306541, "lng": 3.373531},
                        },
                    },
                    "place_id": "ChIJlU6obgaNOxARyywGvjG_Js4",
                    "types": ["political", "sublocality", "sublocality_level_1"],
                },
                {
                    "address_components": [
                        {
                            "long_name": "102216",
                            "short_name": "102216",
                            "types": ["postal_code"],
                        },
                        {
                            "long_name": "Lagos",
                            "short_name": "Lagos",
                            "types": ["locality", "political"],
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
                    ],
                    "formatted_address": "Lagos 102216, Lagos, Nigeria",
                    "geometry": {
                        "bounds": {
                            "northeast": {"lat": 6.558478999999999, "lng": 3.405261},
                            "southwest": {"lat": 6.5234789, "lng": 3.366865},
                        },
                        "location": {"lat": 6.5403253, "lng": 3.3842473},
                        "location_type": "APPROXIMATE",
                        "viewport": {
                            "northeast": {"lat": 6.558478999999999, "lng": 3.405261},
                            "southwest": {"lat": 6.5234789, "lng": 3.366865},
                        },
                    },
                    "place_id": "ChIJq7RKJQyNOxARFW557gJddbM",
                    "types": ["postal_code"],
                },
                {
                    "address_components": [
                        {
                            "long_name": "Shomolu",
                            "short_name": "Shomolu",
                            "types": ["administrative_area_level_2", "political"],
                        },
                        {
                            "long_name": "Ikeja",
                            "short_name": "Ikeja",
                            "types": ["locality", "political"],
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
                    "formatted_address": "Shomolu 102216, Lagos, Nigeria",
                    "geometry": {
                        "bounds": {
                            "northeast": {"lat": 6.5585, "lng": 3.4015},
                            "southwest": {"lat": 6.523499999999999, "lng": 3.3669},
                        },
                        "location": {"lat": 6.5403253, "lng": 3.3842473},
                        "location_type": "APPROXIMATE",
                        "viewport": {
                            "northeast": {"lat": 6.5585, "lng": 3.4015},
                            "southwest": {"lat": 6.523499999999999, "lng": 3.3669},
                        },
                    },
                    "place_id": "ChIJ8RAlRg6NOxARJYGn_NRK4rA",
                    "types": ["administrative_area_level_2", "political"],
                },
                {
                    "address_components": [
                        {
                            "long_name": "Somolu",
                            "short_name": "Somolu",
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
                            "long_name": "Lagos",
                            "short_name": "LA",
                            "types": ["administrative_area_level_1", "political"],
                        },
                        {
                            "long_name": "Nigeria",
                            "short_name": "NG",
                            "types": ["country", "political"],
                        },
                    ],
                    "formatted_address": "Somolu, Lagos, Nigeria",
                    "geometry": {
                        "bounds": {
                            "northeast": {"lat": 6.5584824, "lng": 3.4044428},
                            "southwest": {"lat": 6.516709499999999, "lng": 3.3669714},
                        },
                        "location": {"lat": 6.539173, "lng": 3.3841676},
                        "location_type": "APPROXIMATE",
                        "viewport": {
                            "northeast": {"lat": 6.5584824, "lng": 3.4044428},
                            "southwest": {"lat": 6.516709499999999, "lng": 3.3669714},
                        },
                    },
                    "place_id": "ChIJPf76DxONOxARsjgFx69zQ70",
                    "types": ["political", "sublocality", "sublocality_level_1"],
                },
                {
                    "address_components": [
                        {
                            "long_name": "Ikeja",
                            "short_name": "Ikeja",
                            "types": ["locality", "political"],
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
                    ],
                    "formatted_address": "Ikeja, Lagos, Nigeria",
                    "geometry": {
                        "bounds": {
                            "northeast": {"lat": 6.629741, "lng": 3.436741},
                            "southwest": {"lat": 6.4293299, "lng": 3.290317},
                        },
                        "location": {"lat": 6.601838, "lng": 3.3514863},
                        "location_type": "APPROXIMATE",
                        "viewport": {
                            "northeast": {"lat": 6.629741, "lng": 3.436741},
                            "southwest": {"lat": 6.4293299, "lng": 3.290317},
                        },
                    },
                    "place_id": "ChIJmTkq-iiSOxAR8KG73UsyqNc",
                    "types": ["locality", "political"],
                },
                {
                    "address_components": [
                        {
                            "long_name": "Lagos",
                            "short_name": "Lagos",
                            "types": ["locality", "political"],
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
                    ],
                    "formatted_address": "Lagos, Nigeria",
                    "geometry": {
                        "bounds": {
                            "northeast": {"lat": 6.7027591, "lng": 3.4696459},
                            "southwest": {"lat": 6.393351099999999, "lng": 3.0982732},
                        },
                        "location": {"lat": 6.5243793, "lng": 3.3792057},
                        "location_type": "APPROXIMATE",
                        "viewport": {
                            "northeast": {"lat": 6.7027591, "lng": 3.4696459},
                            "southwest": {"lat": 6.393351099999999, "lng": 3.0982732},
                        },
                    },
                    "place_id": "ChIJwYCC5iqLOxARy9nDZ6OHntw",
                    "types": ["locality", "political"],
                },
                {
                    "address_components": [
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
                    ],
                    "formatted_address": "Lagos, Nigeria",
                    "geometry": {
                        "bounds": {
                            "northeast": {"lat": 6.7004, "lng": 4.3685999},
                            "southwest": {"lat": 6.3678, "lng": 2.705461},
                        },
                        "location": {"lat": 6.522704399999999, "lng": 3.6217802},
                        "location_type": "APPROXIMATE",
                        "viewport": {
                            "northeast": {"lat": 6.7004, "lng": 4.3685999},
                            "southwest": {"lat": 6.3678, "lng": 2.705461},
                        },
                    },
                    "place_id": "ChIJDVUn4rryOxAR1om-G3-tcec",
                    "types": ["administrative_area_level_1", "political"],
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
        }
        if sample_response:
            return sample_response
        response = requests.get(url)
        return response.json()

    @classmethod
    def get_distance_matrix(cls, origin_latlng, destination_latlng, mode="driving"):
        url = f"{cls.BASE_URL}/distancematrix/json?origins={origin_latlng}&destinations={destination_latlng}&mode={mode}&key={cls.SECRET_KEY}"
        sample_response = {
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
        }
        if sample_response:
            return sample_response
        response = requests.get(url)
        return response.json()
