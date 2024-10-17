from app.schemas.misc import Language

org_name_mapping: dict[Language, dict[str, dict[str, str]]] = {
    Language.NLD: {
        "ap": {
            "name": "Autoriteit Persoonsgegevens",
            "code": "autoriteit-persoonsgegevens",
        },
        "buza": {"name": "Ministerie van Buitenlandse Zaken", "code": "ministerie-bz"},
        "bz": {"name": "Ministerie van Buitenlandse Zaken", "code": "ministerie-bz"},
        "bzk": {
            "name": "Ministerie van Binnenlandse Zaken en Koninkrijksrelaties",
            "code": "ministerie-bzk",
        },
        "cbr": {
            "name": "Centraal Bureau Rijvaardigheidsbewijzen",
            "code": "centraal-bureau-rijvaardigheidsbewijzen",
        },
        "cjib": {
            "name": "Centraal Justitieel Incassobureau",
            "code": "centraal-justitieel-incassobureau",
        },
        "ind": {"name": "IND", "code": "ind"},
        "jenv": {
            "name": "Ministerie van Justitie en Veiligheid",
            "code": "ministerie-jenv",
        },
        "kvk": {"name": "Kamer van Koophandel", "code": "kamer-van-koophandel"},
        "minbz": {
            "name": "Ministerie van Buitenlandse Zaken",
            "code": "ministerie-buza",
        },
        "minbzk": {
            "name": "Ministerie van Binnenlandse Zaken en Koninkrijksrelaties",
            "code": "ministerie-bzk",
        },
        "minjenv": {
            "name": "Ministerie van Justitie en Veiligheid",
            "code": "ministerie-jenv",
        },
        "minocw": {
            "name": "Ministerie van Onderwijs, Cultuur en Wetenschap",
            "code": "inspectie-van-het-onderwijs",
        },
        "minvws": {
            "name": "Ministerie van Volksgezondheid, Welzijn en Sport",
            "code": "ministerie-vws",
        },
        "nfi": {
            "name": "Nederlands Forensisch Instituut",
            "code": "nederlands-forensisch-instituut",
        },
        "ocw": {
            "name": "Ministerie van Onderwijs, Cultuur en Wetenschap",
            "code": "inspectie-van-het-onderwijs",
        },
        "rvdk": {
            "name": "Raad voor de Kinderbescherming",
            "code": "raad-kinderbescherming",
        },
        "rvig": {"name": "Rijksdienst voor Identiteitsgegevens", "code": "rvig"},
        "rvo": {
            "name": "Rijksdienst voor Ondernemend Nederland",
            "code": "rijksdienst-voor-ondernemend-nederland",
        },
        "rvr": {
            "name": "Raad voor Rechtsbijstand",
            "code": "raad-voor-de-rechtsbijstand",
        },
        "svb": {"name": "Sociale Verzekeringsbank", "code": "sociale-verzekeringsbank"},
        "szw": {
            "name": "Ministerie van Sociale Zaken en Werkgelegenheid",
            "code": "ministerie-szw",
        },
        "uwv": {
            "name": "Uitvoeringsinstituut Werknemersverzekeringen",
            "code": "uitvoeringsinstituut-werknemersverzekeringen",
        },
        "vws": {
            "name": "Ministerie van Volksgezondheid, Welzijn en Sport",
            "code": "ministerie-vws",
        },
    },
    Language.ENG: {
        "ap": {
            "name": "Dutch Data Protection Authority",
            "code": "autoriteit-persoonsgegevens",
        },
        "buza": {"name": "Ministry of Foreign Affairs", "code": "ministerie-bz"},
        "bz": {"name": "Ministry of Foreign Affairs", "code": "ministerie-bz"},
        "bzk": {
            "name": "Ministry of the Interior and Kingdom Relations",
            "code": "ministerie-bzk",
        },
        "cbr": {
            "name": "Central Office for Motor Vehicle Driver Testing",
            "code": "centraal-bureau-rijvaardigheidsbewijzen",
        },
        "cjib": {
            "name": "Central Judicial Collection Agency",
            "code": "centraal-justitieel-incassobureau",
        },
        "ind": {"name": "IND", "code": "ind"},
        "jenv": {"name": "Ministry of Justice and Security", "code": "ministerie-jenv"},
        "kvk": {"name": "Chamber of Commerce", "code": "kamer-van-koophandel"},
        "minbz": {"name": "Ministry of Foreign Affairs", "code": "ministerie-bz"},
        "minbzk": {
            "name": "Ministry of the Interior and Kingdom Relations",
            "code": "ministerie-bzk",
        },
        "minjenv": {
            "name": "Ministry of Justice and Security",
            "code": "ministerie-jenv",
        },
        "minocw": {
            "name": "Ministry of Education, Culture and Science",
            "code": "inspectie-van-het-onderwijs",
        },
        "minvws": {
            "name": "Ministerie van Volksgezondheid, Welzijn en Sport",
            "code": "ministerie-vws",
        },
        "nfi": {
            "name": "Netherlands Forensic Institute",
            "code": "nederlands-forensisch-instituut",
        },
        "ocw": {
            "name": "Ministry of Education, Culture and Science",
            "code": "inspectie-van-het-onderwijs",
        },
        "rvdk": {
            "name": "Child Care and Protection Board",
            "code": "raad-kinderbescherming",
        },
        "rvig": {"name": "Identity and Passport Service", "code": "rvig"},
        "rvo": {
            "name": "Netherlands Enterprise Agency",
            "code": "rijksdienst-voor-ondernemend-nederland",
        },
        "rvr": {"name": "Council Legal Aid", "code": "raad-voor-de-rechtsbijstand"},
        "svb": {"name": "Social Insurance Bank", "code": "sociale-verzekeringsbank"},
        "szw": {
            "name": "Ministry of Social Affairs and Employment",
            "code": "ministerie-szw",
        },
        "uwv": {
            "name": "Employee Insurance Agency",
            "code": "uitvoeringsinstituut-werknemersverzekeringen",
        },
        "vws": {
            "name": "Ministry of Health Welfare and Sport",
            "code": "ministerie-vws",
        },
    },
    Language.FRY: {
        "ap": {
            "name": "Autoriteit Persoansgegevens",
            "code": "autoriteit-persoonsgegevens",
        },
        "buza": {"name": "ministearje fan útlânske saken", "code": "ministerie-bz"},
        "bz": {"name": "ministearje fan útlânske saken", "code": "ministerie-bz"},
        "bzk": {
            "name": "Ministearje fan Ynlânske Saken en Keninkryksrelaasjes",
            "code": "ministerie-bzk",
        },
        "cbr": {
            "name": "Sintraal Buro Rydfeardigensbewizen",
            "code": "centraal-bureau-rijvaardigheidsbewijzen",
        },
        "cjib": {
            "name": "Sintraal Justysjeel Ynkassoburo",
            "code": "centraal-justitieel-incassobureau",
        },
        "ind": {"name": "IND", "code": "ind"},
        "jenv": {
            "name": "Ministearje fan Justysje en Feiligens",
            "code": "ministerie-jenv",
        },
        "kvk": {"name": "Keamer fan Keaphannel", "code": "kamer-van-koophandel"},
        "minbz": {"name": "ministearje fan útlânske saken", "code": "ministerie-bz"},
        "minbzk": {
            "name": "Ministearje fan Ynlânske Saken en Keninkryksrelaasjes",
            "code": "ministerie-bzk",
        },
        "minjenv": {
            "name": "Ministearje fan Justysje en Feiligens",
            "code": "ministerie-jenv",
        },
        "minocw": {
            "name": "Ministearje fan Underwiis, Kultuer en Wittenskip",
            "code": "inspectie-van-het-onderwijs",
        },
        "minvws": {
            "name": "Ministearje fan Folkssûnens, Wolwêzen en Sport",
            "code": "ministerie-vws",
        },
        "nfi": {
            "name": "Nederlânsk Forensysk Ynstitút",
            "code": "nederlands-forensisch-instituut",
        },
        "ocw": {
            "name": "Ministearje fan Underwiis, Kultuer en Wittenskip",
            "code": "inspectie-van-het-onderwijs",
        },
        "rvdk": {
            "name": "Bernebeskerming Ried",
            "code": "raad-kinderbescherming",
        },
        "rvo": {
            "name": "Netherlands Enterprise Agency",
            "code": "rijksdienst-voor-ondernemend-nederland",
        },
        "rvr": {
            "name": "Bestjoer foar juridyske help",
            "code": "raad-voor-de-rechtsbijstand",
        },
        "svb": {"name": "Sosjale fersekeringsbank", "code": "sociale-verzekeringsbank"},
        "szw": {
            "name": "Ministearje fan Sosjale Saken en Wurkgelegenheid",
            "code": "ministerie-szw",
        },
        "uwv": {
            "name": "Ynstitút foar Employee Insurance",
            "code": "uitvoeringsinstituut-werknemersverzekeringen",
        },
        "vws": {
            "name": "Ministearje fan Folkssûnens, Wolwêzen en Sport",
            "code": "ministerie-vws",
        },
    },
}
