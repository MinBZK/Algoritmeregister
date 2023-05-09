from typing import TypedDict
from app import schemas

default_responses = {
    401: {"description": "Authentication Error", "model": schemas.Message},
    404: {"description": "Not Found Error", "model": schemas.Message},
}

responses = {
    "get_all": {
        **default_responses,
        200: {
            "content": {
                "application/json": {"schema": {"title": "List of algorithm summaries"}}
            }
        },
    },
    "get_one": {
        **default_responses,
        200: {
            "content": {
                "application/json": {
                    "schema": {"title": "Any of the algorithm standards."}
                }
            }
        },
    },
    "get_one_published": {
        **default_responses,
        200: {
            "content": {
                "application/json": {
                    "schema": {"title": "Any of the algorithm standards."}
                }
            }
        },
    },
    "post": {**default_responses},
    "put": {**default_responses},
    "delete": {**default_responses},
    "publish": {**default_responses},
    "release": {**default_responses},
    "preview": {**default_responses},
    "remove": {**default_responses},
}


class EndpointText(TypedDict):
    summary: str
    description: str


api_text: dict[str, EndpointText] = {
    "get_all": {
        "summary": "Haal alle beschikbare algoritmes op.",
        "description": "Geeft een samenvatting van de algoritmes terug waar u bewerkingsrechten voor heeft.",
    },
    "get_one": {
        "summary": "Haal de nieuwste versie van één algoritme op.",
        "description": """Verkrijg de nieuwste gegevens van één algoritme. Dit is niet per se gepubliceerd.""",
    },
    "get_one_published": {
        "summary": "Haal de gepubliceerde versie van één algoritme op.",
        "description": "Verkrijg de gepubliceerde versie van één algoritme.",
    },
    "post": {
        "summary": "Maak een nieuw algoritme.",
        "description": "Het aanroepen van dit endpoint creeërt een nieuw algoritme.",
    },
    "put": {
        "summary": "Update een algoritme.",
        "description": "Sla de nieuwe algoritme-informatie op. Hiermee is het nog niet gepubliceerd.",
    },
    "delete": {
        "summary": "Verberg een algoritme.",
        "description": "Verberg een algoritme, zodat deze niet meer publiek toegankelijk is.",
    },
    "publish": {
        "summary": "Publiceer een algoritme.",
        "description": "Publiceer de laatste gegevens van een algoritme, zodat deze publiek toegankelijk zijn.",
    },
    "release": {
        "summary": "Geef een algoritme vrij voor publicatie.",
        "description": "Geef de laatste gegevens van een algoritme vrij, zodat BZK ze kan gaan inspecteren, en "
        "uiteindelijk publiceren.",
    },
    "preview": {
        "summary": "Bekijk een preview van een algoritme.",
        "description": """Krijg een URL waarmee de laatste gegevens van een algoritme kunnen worden bekeken.""",
    },
    "remove": {
        "summary": "Verwijder een algoritme. Alleen beschikbaar voor beheerders.",
        "description": "",
    },
}
