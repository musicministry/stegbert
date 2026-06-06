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
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "567 - Holy, Holy, Holy! Lord God Almighty!",

    "Responsorial Psalm": "R&A p. 96 - https://www.youtube.com/watch?v=4CipytWuv0c",
    "Gospel Acclamation": "R&A p. 97 - https://www.youtube.com/watch?v=djexyE_j_D0",

    "Offertory": "615 - Holy God, We Praise Thy Name",
    "Communion": "642 - What Wondrous Love Is This",
    "Meditation": "580 - For God So Loved the World",
    "Recessional": "566 - O God, Almighty Father"
}

corpus_christi = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "616 - Praise to the Lord, the Almighty",

    "Responsorial Psalm": "R&A p. 98 - https://www.youtube.com/watch?v=2lyxAUr9KUY",
    "Gospel Acclamation": "R&A p. 99 - https://www.youtube.com/watch?v=L0Fb8sDMJXg",

    "Offertory": "932 - One Bread, One Body",
    "Communion": "910 - Shepherd of Souls",
    "Meditation": "619 - Let All Mortal Flesh Keep Silence",
    "Recessional": "615 - Holy God, We Praise Thy Name"
}

ot11 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "688 - O God, Our Help in Ages Past",

    "Responsorial Psalm": "R&A p. 100 - https://www.youtube.com/watch?v=QTxAquatwKk",
    "Gospel Acclamation": "R&A p. 101 - https://www.youtube.com/watch?v=bRqcBEMhUfc",

    "Offertory": "853 - All People That on Earth Do Dwell",
    "Communion": "914 - Lord, Who at Your First Eucharist",
    "Recessional": "544 - Lord, You Give the Great Commission"
}

ot12 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "837 - Gather Your People (Hurd)",

    "Responsorial Psalm": "R&A p. 102 - https://www.youtube.com/watch?v=6Kv7R4_D8pg",
    "Gospel Acclamation": "R&A p. 103 - https://www.youtube.com/watch?v=MfzbAQlcldM",

    "Offertory": "683 - Be Not Afraid (Dufford)",
    "Communion": "920 - Pan de Vida",
    # "Meditation": "693 - All Will Be Well",
    "Recessional": "689 - Though the Mountains May Fall"
}

ot13 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "624 - Lift Up Your Hearts",

    "Responsorial Psalm": "R&A p. 104 - https://www.youtube.com/watch?v=5Xyc1brXyMI",
    "Gospel Acclamation": "R&A p. 105 - https://www.youtube.com/watch?v=rg8DZXFud_s",

    "Offertory": "903 - Baptized in Water",
    "Communion": "914 - Lord, Who at Your First Eucharist",
    "Recessional": "801 - Take Up Your Cross (ERHALT UNS HERR)"
}

ot14 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "855 - Morning Has Broken",

    "Responsorial Psalm": "R&A p. 106 - https://www.youtube.com/watch?v=28_GCyynw-o",
    "Gospel Acclamation": "R&A p. 107 - https://www.youtube.com/watch?v=tN5RCOwvl24",

    "Offertory": "724 - I Heard the Voice of Jesus Say",
    "Communion": "930 - Taste and See (Moore)",
    "Meditation": "720 - Come to Me (Bell)",
    "Recessional": "871 - We Shall Rise Again"
}

ot15 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "838 - Come to the Feast",

    "Responsorial Psalm": "R&A p. 108 - https://www.youtube.com/watch?v=ofki6mUE9Ug",
    "Gospel Acclamation": "R&A p. 109 - https://www.youtube.com/watch?v=h66erAKfn7A",

    "Offertory": "651 - Open My Eyes",
    "Communion": "783 - Unless a Grain of Wheat",
    "Recessional": "644 - There's a Wideness in God's Mercy"
}

