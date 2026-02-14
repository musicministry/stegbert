# =============================================================================
# Other Occasions 2026
# Liturgical Year A
#
# Updated: February 2026
#
# Manually generated hymn data dictionaries
#
# =============================================================================
# Entry template:
#
#     seasonNN = {
#         "Mass": "Mass setting",
#         "parts": ["Gloria", "Holy", "Memorial Acclamation A", "Amen",
#                   "Lamb of God"],
#
#         "Processional":         "NNN - Song Title",
#
#         "Responsorial Psalm":   "R&A p. n - YouTube video URL",
#         "Gospel Acclamation":   "R&A p. n - YouTube video URL",
#
#         "Preparation of Gifts": "NNN - Song Title",
#         "Communion":            "NNN - Song Title",
#         "Recessional":          "NNN - Song Title",
#     }
#
# Repeat this YAML block for each liturgy -- but be sure to give each block a
# unique name that matches a `feast` name in the liturgical calendar dataframe.
# "Mass" (str) and "parts" (list of strings) are required. Other keys can be
# anything or as many as desired. These will be rendered in the order in which
# they appear here. Replace N and NNN with page or hymnal song numbers.
#
# =============================================================================

confirmation = {
    "season": "Lent",
    "date": "2026-03-07 11:00",

    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Cantus Missae (B)"
    ],

    "Processional": "601 - Laudate, Laudate Dominum",

    "Responsorial Psalm": "R&A p. 50 - https://youtu.be/YeKe01s4loE?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation": "Handout - Handout",

    "Anointing with Chrism": "NA - organ interlude, if desired",
    "Offertory": "553 - O Spirit All-Embracing",
    "Communion": "920 - Pan de Vida",
    "Recessional": "686 - Blest Be the Lord"
}
