# =============================================================================
# Ordinary Time 2026
# Liturgical Year A
#
# Updated January 2026
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
#         "RA": [N, N],
#         "Responsorial Psalm":   "YouTube video URL",
#         "Gospel Acclamation":   "YouTube video URL",
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

ot02 = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "766 - City of God",

    "RA": [32, 33],
    "Responsorial Psalm":   "https://youtu.be/WrYH58H4Qgo?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "https://youtu.be/GfmISUff9ao?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "777 - Here I Am, Lord (Schutte)",
    "Communion":            "939 - Behold the Lamb",
    "Recessional":          "773 - You Have Anointed Me"
}

ot03 = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "607 - Sing a New Song",

    "RA": [34, 35],
    "Responsorial Psalm":   "https://youtu.be/bTYaj28lh1g?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "https://youtu.be/_cFM_Ootlso?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "781 - Lord, When You Came to the Seashore",
    "Communion":            "834 - We Are Many Parts",
    "Recessional":          "766 - City of God"
}

ot04 = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "848 - Gather Us In",

    "RA": [36, 37],
    "Responsorial Psalm":   "https://youtu.be/P84D_d_at8s?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "https://youtu.be/85cW9k6ycEI?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "658 - Seek Ye First",
    "Communion":            "47 - The Cry of the Poor",
    "Recessional":          "592 - We Are the Light of the World"
}

ot05 = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "590 - Christ, Be Our Light",

    "RA": [38, 39],
    "Responsorial Psalm":   "https://youtu.be/FIEB_jG1qKY?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "https://youtu.be/KQIBIVOKfh8?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "478 - Return to God",
    "Communion":            "592 - We Are the Light of the World",
    "Recessional":          "775 - Go Make a Difference"
}

ot06 = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "611 - All Creatures of Our God and King",

    "RA": [40, 41],
    "Responsorial Psalm":   "https://youtu.be/4xHCHwQxJN0?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "https://youtu.be/-4oHL_ujLMQ?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "612 - When In Our Music God is Glorified",
    "Communion":            "728 - Eye Has Not Seen",
    "Recessional":          "949 - Alleluia! Sing to Jesus"
}
