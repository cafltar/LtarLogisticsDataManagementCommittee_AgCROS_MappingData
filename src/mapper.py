class Mapper:
    CROP_ABBRIV_TO_AGCROS = {
        "SW": "Triticum aestivum (Spring Wheat)",
        "WW": "Triticum aestivum (Winter Wheat)",
        "SC": "Brassica napus (Spring Canola)",
        "WC": "Brassica napus (Winter Canola)",
        "SB": "Hordeum vulgare (Spring Barley)",
        "SP": "Pisum sativum (Spring Pea)",
        "WB": "Hordeum vulgare (Winter Barley)",
        "WP": "Pisum sativum (Winter Pea)",
        "WT": "Triticum durum (Winter Triticale)",
        "WL": "Lens culinaris (Winter Lentil)",
        "GB": "Cicer arietinum (Garbonzo Beans)",
        "AL": "Medicago sativa (Alfalfa)",
        "CF": "Fallow"
    }

    FIELDSTRIP_TO_TREATMENTID = {
        "C8": "C5",
        "C7": "C6"
    }
    FIELDSTRIP_ABBRIV_TO_FIELDSTRIP_LIST = {
        "A": "A1, A2, A3, A4, A5, A6",
        "B": "B1, B2, B3, B4, B5, B6",
        "C": "C1, C2, C3, C4, C5, C6, C7, C8",
        "(all)": "A1, A2, A3, A4, A5, A6, B1, B2, B3, B4, B5, B6, C1, C2, C3, C4, C5, C6, C7, C8"
    }
    DRILL_CONFIG_TO_PLANTING_METHOD_AGCROS = {
        "uniform": "Row",
        "broadcast": "Broadcast",
        "paired row": "Twin Row"
    }
