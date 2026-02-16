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

ot02 = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "766 - City of God",

    "Responsorial Psalm":   "R&A p. 32 - https://youtu.be/WrYH58H4Qgo?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "R&A p. 33 - https://youtu.be/GfmISUff9ao?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "777 - Here I Am, Lord",
    "Communion":            "939 - Behold the Lamb",
    "Recessional":          "773 - You Have Anointed Me"
}

ot03 = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "607 - Sing a New Song (Schutte)",

    "Responsorial Psalm":   "R&A p. 34 - https://youtu.be/bTYaj28lh1g?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "R&A p. 35 - https://youtu.be/_cFM_Ootlso?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "781 - Lord, When You Came",
    "Communion":            "834 - We Are Many Parts",
    "Recessional":          "766 - City of God"
}

ot04 = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "848 - Gather Us In",

    "Responsorial Psalm":   "R&A p. 36 - https://youtu.be/P84D_d_at8s?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "R&A p. 37 - https://youtu.be/85cW9k6ycEI?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "658 - Seek Ye First",
    "Communion":            "47 - Psalm 34: The Cry of the Poor",
    "Recessional":          "592 - We Are the Light of the World"
}

ot05 = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "590 - Christ, Be Our Light",

    "Responsorial Psalm":   "R&A p. 38 - https://youtu.be/FIEB_jG1qKY?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "R&A p. 39 - https://youtu.be/KQIBIVOKfh8?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "478 - Return to God",
    "Communion":            "592 - We Are the Light of the World",
    "Recessional":          "775 - Go Make a Difference"
}

ot06 = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "611 - All Creatures of Our God and King",

    "Responsorial Psalm":   "R&A p. 40 - https://youtu.be/4xHCHwQxJN0?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "R&A p. 41 - https://youtu.be/-4oHL_ujLMQ?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "612 - When In Our Music God is Glorified",
    "Communion":            "728 - Eye Has Not Seen",
    "Recessional":          "949 - Alleluia! Sing to Jesus"
}


holy_trinity = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Mass of St. Dymphna",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "567 - Holy, Holy, Holy! Lord God Almighty!",

    "Responsorial Psalm": "R&A p. 96 - https://youtu.be/4CipytWuv0c?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation": "R&A p. 97 - https://youtu.be/djexyE_j_D0?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Offertory": "615 - Holy God, We Praise Thy Name",
    "Communion": "642 - What Wondrous Love Is This",
    "Recessional": "566 - O God, Almighty Father"
}

corpus_christi = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Mass of St. Dymphna",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "616 - Praise to the Lord, the Almighty",

    "Responsorial Psalm": "R&A p. 98 - https://youtu.be/2lyxAUr9KUY?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation": "R&A p. 99 - https://youtu.be/L0Fb8sDMJXg?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Offertory": "932 - One Bread, One Body",
    "Communion": "910 - Shepherd of Souls",
    "Meditation": "619 - Let All Mortal Flesh Keep Silence",
    "Recessional": "615 - Holy God, We Praise Thy Name"
}
