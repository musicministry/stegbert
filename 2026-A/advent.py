# =============================================================================
# Advent 2025
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

advent01 = {
    "Mass": "Missa Emmanuel",
    "parts": ["Holy: Missa Emmanuel", "Memorial Acclamation A: Missa Emmanuel", "Amen: Missa Emmanuel", "Lamb of God: Missa Emmanuel"],

    "Processional":         "577 - Sing Out, Earth and Skies!",

    "Responsorial Psalm":   "R&A p. 4 - https://youtu.be/4yPHj2DFoC4?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "R&A p. 5 - https://youtu.be/6JGogB_Mb-I?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "423 - Awake! Awake, and Greet the New Morn",
    "Communion":            "397 - Maranatha, Lord Messiah",
    "Recessional":          "766 - City of God"
}

# =============================================================================

advent02 = {
    "Mass": "Missa Emmanuel",
    "parts": ["Holy: Missa Emmanuel", "Memorial Acclamation A: Missa Emmanuel", "Amen: Missa Emmanuel", "Lamb of God: Missa Emmanuel"],

    "Processional":          "418 - On Jordan's Bank",

    "Responsorial Psalm":    "R&A p. 6 - https://youtu.be/KlaXFWpN7n4?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":    "R&A p. 7 - https://youtu.be/EFvpHsLDBOU?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    
    "Preparation of Gifts": "421 - Savior of the Nations, Come",
    "Communion":            "397 - Maranatha, Lord Messiah",
    "Recessional":          "409 - People, Look East"
}

# =============================================================================

advent03 = {
    "Mass": "Missa Emmanuel",
    "parts": ["Holy: Missa Emmanuel", "Memorial Acclamation A: Missa Emmanuel", "Amen: Missa Emmanuel", "Lamb of God: Missa Emmanuel"],

    "Processional":         "404 - When the King Shall Come Again",

    "Responsorial Psalm":   "R&A p. 12 - https://youtu.be/WOw1ZGgmceM?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "R&A p. 13 - https://youtu.be/4rLyhdT6kMg?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    
    "Preparation of Gifts": "395 - O Come, O Come, Emmanuel",
    "Communion":            "397 - Maranatha, Lord Messiah",
    "Recessional":          "423 - Awake! Awake, and Greet the New Morn"
}

# =============================================================================

advent04 = {
    "Mass": "Missa Emmanuel",
    "parts": ["Holy: Missa Emmanuel", "Memorial Acclamation A: Missa Emmanuel", "Amen: Missa Emmanuel", "Lamb of God: Missa Emmanuel"],

    "Processional":         "401 - O Come, Divine Messiah",

    "Responsorial Psalm":   "R&A p. 14 - https://youtu.be/eTn_fK_16_4?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "R&A p. 15 - https://youtu.be/mDRuiP8oB8s?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    
    "Preparation of Gifts": "395 - O Come, O Come, Emmanuel",
    "Communion":            "414 - The King Shall Come When Morning Dawns (Morning Song)",
    "Recessional":          "572 - The King of Glory"
}

# =============================================================================
# Update 12/8:
# Preparation changed to "Creator of the Stars of Night" and communion to
# "Mary, Did You Know?" to accomodate school Mass request. Spoken psalm.

immaculate_conception = {
    "Mass": "Heritage Mass",
    "parts": ["Gloria: Heritage Mass", "Holy: Heritage Mass", "Memorial Acclamation A: Heritage Mass", "Amen: Heritage Mass", "Lamb of God: Heritage Mass"],

    "Processional":         "886 - Immaculate Mary",
    
    "Responsorial Psalm":   "R&A p. 8 - https://youtu.be/Bk_8VhRGweU?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",
    "Gospel Acclamation":   "R&A p. 9 - https://youtu.be/F2YKiu3hbEY?list=PL1_lMtcpfrcloo19ceGJAEXPuXK2LS4os",

    "Preparation of Gifts": "875 - Praise We the Lord This Day",
    "Communion":            "100 - Luke 1:46-53: My Soul Gives Glory",
    "Recessional":          "458 - I Sing a Maid"
}

# =============================================================================
