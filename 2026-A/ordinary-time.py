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

ot16 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "848 - Gather Us In",

    "Responsorial Psalm": "R&A p. 110 - https://www.youtube.com/watch?v=nswETou7fuI",
    "Gospel Acclamation": "R&A p. 111 - https://www.youtube.com/watch?v=buvAWjs75Z8",

    "Offertory": "738 - The Reign of God",
    "Communion": "940 - You Satisfy the Hungry Heart",
    "Recessional": "573 - To Jesus Christ, Our Sovereign King"
}

ot17 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "846 - Come, Host of Heaven's High Dwelling Place",

    "Responsorial Psalm": "R&A p. 112 - https://www.youtube.com/watch?v=-33YoEi4COM",
    "Gospel Acclamation": "R&A p. 113 - https://www.youtube.com/watch?v=2-rE3NDO5t4",

    "Offertory": "738 - The Reign of God",
    "Communion": "943 - Bread of Life from Heaven",
    "Recessional": "610 - Sing of the Lord's Goodness"
}

ot18 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "838 - Come to the Feast",

    "Responsorial Psalm": "R&A p. 114 - https://www.youtube.com/watch?v=HgK-IxdOSX4",
    "Gospel Acclamation": "R&A p. 115 - https://www.youtube.com/watch?v=UbYeJMl7fEU",

    "Offertory": "738 - The Reign of God",
    "Communion": "945 - I Am the Bread of Life",
    "Recessional": "641 - Love Divine, All Loves Excelling"
}

ot19 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "689 - Though the Mountains May Fall",

    "Responsorial Psalm": "R&A p. 116 - https://www.youtube.com/watch?v=FLVxPSQqAHM",
    "Gospel Acclamation": "R&A p. 117 - https://www.youtube.com/watch?v=_LG-5UnrdVo",

    "Offertory": "694 - How Firm a Foundation",
    "Communion": "940 - You Satisfy the Hungry Heart",
    "Recessional": "NA - Eternal Father, Strong to Save"
}

# assumption = {
#     "Mass": "Mass of St. Dymphna",
#     "parts": [
#         "Gloria: Heritage Mass",
#         "Holy: Mass of St. Dymphna",
#         "Memorial Acclamation A: Mass of St. Dymphna",
#         "Amen: Mass of St. Dymphna",
#         "Lamb of God: Mass of St. Dymphna"
#     ],

#     "Processional": "886 - Immaculate Mary",

#     "Responsorial Psalm": "R&A p. 120 - https://www.youtube.com/watch?v=LLbtJQdjC8M",
#     "Gospel Acclamation": "R&A p. 121 - https://www.youtube.com/watch?v=oC3ENLBOOJs",

#     "Offertory": "100 - Luke 1:46-53: My Soul Gives Glory",
#     "Communion": "895 - O Sanctíssima",
#     "Recessional": "457 - Sing of Mary, Pure and Lowly"
# }

ot20 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "839 - As We Gather at Your Table",

    "Responsorial Psalm": "R&A p. 122 - https://www.youtube.com/watch?v=jtK9oRoguTI",
    "Gospel Acclamation": "R&A p. 123 - https://www.youtube.com/watch?v=uOB3hMpQZMg",

    "Offertory": "657 - We Cannot Measure How You Heal",
    "Communion": "946 - Let Us Be Bread",
    "Recessional": "644 - There's a Wideness in God's Mercy"
}

ot21 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "742 - The Church's One Foundation",

    "Responsorial Psalm": "R&A p. 124 - https://www.youtube.com/watch?v=yw4rEt7tYP0",
    "Gospel Acclamation": "R&A p. 125 - https://www.youtube.com/watch?v=v_0znl05wVQ",

    "Offertory": "744 - As a Fire Is Meant for Burning",
    "Communion": "916 - I Receive the Living God",
    "Recessional": "743 - Sing a New Church"
}

ot22 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "801 - Take Up Your Cross (ERHALT UNS HERR)",

    "Responsorial Psalm": "R&A p. 126 - https://www.youtube.com/watch?v=BuKPQSNRHFU",
    "Gospel Acclamation": "R&A p. 127 - https://www.youtube.com/watch?v=NphDrmPbTtw",

    "Offertory": "790 - The Summons",
    "Meditation": "783 - Unless a Grain of Wheat",
    "Recessional": "881 - Lift High the Cross"
}

ot23 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "839 - As We Gather at Your Table",

    "Responsorial Psalm": "R&A p. 128 - https://www.youtube.com/watch?v=QIkxJnZq-Bc",
    "Gospel Acclamation": "R&A p. 129 - https://www.youtube.com/watch?v=4yXRUxMug3c",

    "Offertory": "907 - Where Two or Three Are Gathered",
    "Communion": "943 - Bread of Life from Heaven",
    "Meditation": "651 - Open My Eyes",
    "Recessional": "736 - The Kingdom of God (LAUDATE DOMINUM)"
}

ot24 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "964 - The Master Came to Bring Good News",

    "Responsorial Psalm": "R&A p. 130 - https://www.youtube.com/watch?v=om5nZn84FqI",
    "Gospel Acclamation": "R&A p. 131 - https://www.youtube.com/watch?v=I4NOd5OG9Lc",

    "Offertory": "751 - The Servant Song",
    "Communion": "646 - Keep in Mind",
    "Meditation": "828 - Make Me a Channel of Your Peace",
    "Recessional": "736 - The Kingdom of God (LAUDATE DOMINUM)"
}

ot25 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "606 - Glory and Praise to Our God",

    "Responsorial Psalm": "R&A p. 132 - https://www.youtube.com/watch?v=nv_kGYIElpQ",
    "Gospel Acclamation": "R&A p. 133 - https://www.youtube.com/watch?v=ijQPyEmW8O4",

    "Offertory": "695 - You Are Near",
    "Communion": "588 - I Have Loved You",
    "Meditation": "586 - You Are All We Have",
    "Recessional": "736 - The Kingdom of God (LAUDATE DOMINUM)"
}

ot26 = {
    "Mass": "Mass of St. Dymphna",
    "parts": [
        "Gloria: Heritage Mass",
        "Holy: Mass of St. Dymphna",
        "Memorial Acclamation A: Mass of St. Dymphna",
        "Amen: Mass of St. Dymphna",
        "Lamb of God: Mass of St. Dymphna"
    ],

    "Processional": "570 - All Hail the Power of Jesus' Name!",

    "Responsorial Psalm": "R&A p. 134 - https://www.youtube.com/watch?v=kWe_moiMLHo",
    "Gospel Acclamation": "R&A p. 135 - https://www.youtube.com/watch?v=EOp3gMrvOyE",

    "Offertory": "703 - Lord of All Nations, Grant Me Grace",
    "Communion": "907 - Where Two or Three Are Gathered",
    "Recessional": "573 - To Jesus Christ, Our Sovereign King"
}
