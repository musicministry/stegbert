# =============================================================================
# Christmas 2025
# Liturgical Year A
#
# Updated December 2025
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

christmas_day = {
    "Mass": "Christmas Carol Mass",
    "parts": ["Gloria: A Christmas Gloria", "Holy: Christmas Carol Mass", "Memorial Acclamation C: Christmas Carol Mass", "Amen: Christmas Carol Mass", "Lamb of God: Christmas Carol Mass"],

    "Processional":         "439 - O Come, All Ye Faithful",

    "RA": [22, 23],
    "Responsorial Psalm":   "70 - Psalm 98: All the Ends of the Earth (Haas/Haugen)",
    "Gospel Acclamation":   "https://youtu.be/KxUt7PyXNYk?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "424 - Hark! The Herald Angels Sing",
    "Communion":            "432 - Nativity Carol",
    "Meditation":           "441 - Silent Night",
    "Recessional":          "437 - Joy to the World"
}

holy_family = {
    "Mass": "Christmas Carol Mass",
    "parts": ["Gloria: A Christmas Gloria", "Holy: Christmas Carol Mass", "Memorial Acclamation C: Christmas Carol Mass", "Amen: Christmas Carol Mass", "Lamb of God: Christmas Carol Mass"],

    "Processional":         "438 - Angels, from the Realms of Glory",

    "RA": [24, 25],
    "Responsorial Psalm":   "https://youtu.be/4gjqxJ_eL-I?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "https://youtu.be/4gjqxJ_eL-I?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "436 - Wood of the Cradle",
    "Communion":            "455 - Once in Royal David's City",
    "Recessional":          "430 - Angels We Have Heard on High"
}

mary_mother_of_god = {
    "Mass": "Christmas Carol Mass",
    "parts": ["Gloria: A Christmas Gloria", "Holy: Christmas Carol Mass", "Memorial Acclamation C: Christmas Carol Mass", "Amen: Christmas Carol Mass", "Lamb of God: Christmas Carol Mass"],

    "Processional":         "457 - Sing of Mary",

    "RA": [26, 27],
    "Responsorial Psalm":   "https://youtu.be/LcqkBimDhjs?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "https://youtu.be/JuH7sw1sobE?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "448 - Away in a Manger (Mueller)",
    "Communion":            "451 - Lo, How a Rose E'er Blooming",
    "Recessional":          "458 - I Sing a Maid"
}


epiphany = {
    "Mass": "Christmas Carol Mass",
    "parts": ["Gloria: A Christmas Gloria", "Holy: Christmas Carol Mass", "Memorial Acclamation C: Christmas Carol Mass", "Amen: Christmas Carol Mass", "Lamb of God: Christmas Carol Mass"],

    "Processional":         "459 - Songs of Thankfulness and Praise",

    "RA": [28, 29],
    "Responsorial Psalm":   "https://youtu.be/5poRq9YtiIs?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "https://youtu.be/HiKwEUIipX8?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "463 - We Three Kings",
    "Communion":            "460 - The First Nowell",
    "Recessional":          "461 - What Star Is This"
}

baptism = {
    "Mass": "Christmas Carol Mass",
    "parts": ["Gloria: A Christmas Gloria", "Holy: Christmas Carol Mass", "Memorial Acclamation C: Christmas Carol Mass", "Amen: Christmas Carol Mass", "Lamb of God: Christmas Carol Mass"],

    "Processional":         "467 - When John Baptized by Jordan's River",

    "RA": [30, 31],
    "Responsorial Psalm":   "https://youtu.be/UaV7slHh658?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "https://youtu.be/D4l2yvw-2z4?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "440 - Good Christian Friends, Rejoice",
    "Communion":            "423 - Awake! Awake, and Greet the New Morn | (*Christmas lyrics*)",
    "Recessional":          "428 - Go, Tell It on the Mountain"
}