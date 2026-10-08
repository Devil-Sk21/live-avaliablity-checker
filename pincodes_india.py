"""
Dataset of Indian Cities and Pincodes across all 28 States and 8 Union Territories.
"""

INDIA_PINCODES = [
    # --- 28 States ---
    # Andhra Pradesh
    {"state": "Andhra Pradesh", "city": "Visakhapatnam", "pincode": "530001"},
    {"state": "Andhra Pradesh", "city": "Vijayawada", "pincode": "520001"},
    {"state": "Andhra Pradesh", "city": "Guntur", "pincode": "522001"},
    {"state": "Andhra Pradesh", "city": "Tirupati", "pincode": "517501"},
    {"state": "Andhra Pradesh", "city": "Kurnool", "pincode": "518001"},

    # Arunachal Pradesh
    {"state": "Arunachal Pradesh", "city": "Itanagar", "pincode": "791111"},
    {"state": "Arunachal Pradesh", "city": "Naharlagun", "pincode": "791110"},
    {"state": "Arunachal Pradesh", "city": "Pasighat", "pincode": "791102"},

    # Assam
    {"state": "Assam", "city": "Guwahati", "pincode": "781001"},
    {"state": "Assam", "city": "Silchar", "pincode": "788001"},
    {"state": "Assam", "city": "Dibrugarh", "pincode": "786001"},
    {"state": "Assam", "city": "Jorhat", "pincode": "785001"},
    {"state": "Assam", "city": "Tezpur", "pincode": "784001"},

    # Bihar
    {"state": "Bihar", "city": "Patna", "pincode": "800001"},
    {"state": "Bihar", "city": "Gaya", "pincode": "823001"},
    {"state": "Bihar", "city": "Muzaffarpur", "pincode": "842001"},
    {"state": "Bihar", "city": "Bhagalpur", "pincode": "812001"},
    {"state": "Bihar", "city": "Darbhanga", "pincode": "846004"},

    # Chhattisgarh
    {"state": "Chhattisgarh", "city": "Raipur", "pincode": "492001"},
    {"state": "Chhattisgarh", "city": "Bilaspur", "pincode": "495001"},
    {"state": "Chhattisgarh", "city": "Bhilai / Durg", "pincode": "490006"},
    {"state": "Chhattisgarh", "city": "Korba", "pincode": "495677"},

    # Goa
    {"state": "Goa", "city": "Panaji", "pincode": "403001"},
    {"state": "Goa", "city": "Margao", "pincode": "403601"},
    {"state": "Goa", "city": "Vasco da Gama", "pincode": "403802"},
    {"state": "Goa", "city": "Mapusa", "pincode": "403507"},

    # Gujarat
    {"state": "Gujarat", "city": "Ahmedabad", "pincode": "380001"},
    {"state": "Gujarat", "city": "Surat", "pincode": "395001"},
    {"state": "Gujarat", "city": "Vadodara", "pincode": "390001"},
    {"state": "Gujarat", "city": "Rajkot", "pincode": "360001"},
    {"state": "Gujarat", "city": "Gandhinagar", "pincode": "382010"},
    {"state": "Gujarat", "city": "Bhavnagar", "pincode": "364001"},

    # Haryana
    {"state": "Haryana", "city": "Gurugram", "pincode": "122001"},
    {"state": "Haryana", "city": "Faridabad", "pincode": "121001"},
    {"state": "Haryana", "city": "Panipat", "pincode": "132103"},
    {"state": "Haryana", "city": "Ambala", "pincode": "134003"},
    {"state": "Haryana", "city": "Karnal", "pincode": "132001"},
    {"state": "Haryana", "city": "Rohtak", "pincode": "124001"},

    # Himachal Pradesh
    {"state": "Himachal Pradesh", "city": "Shimla", "pincode": "171001"},
    {"state": "Himachal Pradesh", "city": "Dharamshala", "pincode": "176215"},
    {"state": "Himachal Pradesh", "city": "Mandi", "pincode": "175001"},
    {"state": "Himachal Pradesh", "city": "Solan", "pincode": "173212"},
    {"state": "Himachal Pradesh", "city": "Kullu", "pincode": "175101"},

    # Jharkhand
    {"state": "Jharkhand", "city": "Ranchi", "pincode": "834001"},
    {"state": "Jharkhand", "city": "Jamshedpur", "pincode": "831001"},
    {"state": "Jharkhand", "city": "Dhanbad", "pincode": "826001"},
    {"state": "Jharkhand", "city": "Bokaro", "pincode": "827001"},
    {"state": "Jharkhand", "city": "Deoghar", "pincode": "814112"},

    # Karnataka
    {"state": "Karnataka", "city": "Bengaluru", "pincode": "560001"},
    {"state": "Karnataka", "city": "Mysuru", "pincode": "570001"},
    {"state": "Karnataka", "city": "Mangaluru", "pincode": "575001"},
    {"state": "Karnataka", "city": "Hubballi", "pincode": "580020"},
    {"state": "Karnataka", "city": "Belagavi", "pincode": "590001"},

    # Kerala
    {"state": "Kerala", "city": "Thiruvananthapuram", "pincode": "695001"},
    {"state": "Kerala", "city": "Kochi", "pincode": "682001"},
    {"state": "Kerala", "city": "Kozhikode", "pincode": "673001"},
    {"state": "Kerala", "city": "Thrissur", "pincode": "680001"},
    {"state": "Kerala", "city": "Kollam", "pincode": "691001"},

    # Madhya Pradesh
    {"state": "Madhya Pradesh", "city": "Bhopal", "pincode": "462001"},
    {"state": "Madhya Pradesh", "city": "Indore", "pincode": "452001"},
    {"state": "Madhya Pradesh", "city": "Gwalior", "pincode": "474001"},
    {"state": "Madhya Pradesh", "city": "Jabalpur", "pincode": "482001"},
    {"state": "Madhya Pradesh", "city": "Ujjain", "pincode": "456001"},

    # Maharashtra
    {"state": "Maharashtra", "city": "Mumbai", "pincode": "400001"},
    {"state": "Maharashtra", "city": "Pune", "pincode": "411001"},
    {"state": "Maharashtra", "city": "Nagpur", "pincode": "440001"},
    {"state": "Maharashtra", "city": "Nashik", "pincode": "422001"},
    {"state": "Maharashtra", "city": "Thane", "pincode": "400601"},
    {"state": "Maharashtra", "city": "Chhatrapati Sambhajinagar", "pincode": "431001"},

    # Manipur
    {"state": "Manipur", "city": "Imphal", "pincode": "795001"},
    {"state": "Manipur", "city": "Churachandpur", "pincode": "795128"},
    {"state": "Manipur", "city": "Thoubal", "pincode": "795138"},

    # Meghalaya
    {"state": "Meghalaya", "city": "Shillong", "pincode": "793001"},
    {"state": "Meghalaya", "city": "Tura", "pincode": "794001"},
    {"state": "Meghalaya", "city": "Jowai", "pincode": "793150"},

    # Mizoram
    {"state": "Mizoram", "city": "Aizawl", "pincode": "796001"},
    {"state": "Mizoram", "city": "Lunglei", "pincode": "796701"},
    {"state": "Mizoram", "city": "Champhai", "pincode": "796321"},

    # Nagaland
    {"state": "Nagaland", "city": "Kohima", "pincode": "797001"},
    {"state": "Nagaland", "city": "Dimapur", "pincode": "797112"},
    {"state": "Nagaland", "city": "Mokokchung", "pincode": "798601"},

    # Odisha
    {"state": "Odisha", "city": "Bhubaneswar", "pincode": "751001"},
    {"state": "Odisha", "city": "Cuttack", "pincode": "753001"},
    {"state": "Odisha", "city": "Rourkela", "pincode": "769001"},
    {"state": "Odisha", "city": "Puri", "pincode": "752001"},
    {"state": "Odisha", "city": "Sambalpur", "pincode": "768001"},

    # Punjab
    {"state": "Punjab", "city": "Ludhiana", "pincode": "141001"},
    {"state": "Punjab", "city": "Amritsar", "pincode": "143001"},
    {"state": "Punjab", "city": "Jalandhar", "pincode": "144001"},
    {"state": "Punjab", "city": "Patiala", "pincode": "147001"},
    {"state": "Punjab", "city": "Bathinda", "pincode": "151001"},

    # Rajasthan
    {"state": "Rajasthan", "city": "Jaipur", "pincode": "302001"},
    {"state": "Rajasthan", "city": "Jodhpur", "pincode": "342001"},
    {"state": "Rajasthan", "city": "Udaipur", "pincode": "313001"},
    {"state": "Rajasthan", "city": "Kota", "pincode": "324001"},
    {"state": "Rajasthan", "city": "Bikaner", "pincode": "334001"},
    {"state": "Rajasthan", "city": "Ajmer", "pincode": "305001"},

    # Sikkim
    {"state": "Sikkim", "city": "Gangtok", "pincode": "737101"},
    {"state": "Sikkim", "city": "Namchi", "pincode": "737126"},
    {"state": "Sikkim", "city": "Geyzing", "pincode": "737111"},

    # Tamil Nadu
    {"state": "Tamil Nadu", "city": "Chennai", "pincode": "600001"},
    {"state": "Tamil Nadu", "city": "Coimbatore", "pincode": "641001"},
    {"state": "Tamil Nadu", "city": "Madurai", "pincode": "625001"},
    {"state": "Tamil Nadu", "city": "Tiruchirappalli", "pincode": "620001"},
    {"state": "Tamil Nadu", "city": "Salem", "pincode": "636001"},

    # Telangana
    {"state": "Telangana", "city": "Hyderabad", "pincode": "500001"},
    {"state": "Telangana", "city": "Warangal", "pincode": "506001"},
    {"state": "Telangana", "city": "Nizamabad", "pincode": "503001"},
    {"state": "Telangana", "city": "Karimnagar", "pincode": "505001"},
    {"state": "Telangana", "city": "Khammam", "pincode": "507001"},

    # Tripura
    {"state": "Tripura", "city": "Agartala", "pincode": "799001"},
    {"state": "Tripura", "city": "Dharmanagar", "pincode": "799250"},
    {"state": "Tripura", "city": "Udaipur", "pincode": "799120"},

    # Uttar Pradesh
    {"state": "Uttar Pradesh", "city": "Lucknow", "pincode": "226001"},
    {"state": "Uttar Pradesh", "city": "Kanpur", "pincode": "208001"},
    {"state": "Uttar Pradesh", "city": "Noida", "pincode": "201301"},
    {"state": "Uttar Pradesh", "city": "Varanasi", "pincode": "221001"},
    {"state": "Uttar Pradesh", "city": "Agra", "pincode": "282001"},
    {"state": "Uttar Pradesh", "city": "Prayagraj", "pincode": "211001"},
    {"state": "Uttar Pradesh", "city": "Ghaziabad", "pincode": "201001"},
    {"state": "Uttar Pradesh", "city": "Meerut", "pincode": "250001"},

    # Uttarakhand
    {"state": "Uttarakhand", "city": "Dehradun", "pincode": "248001"},
    {"state": "Uttarakhand", "city": "Haridwar", "pincode": "249401"},
    {"state": "Uttarakhand", "city": "Haldwani", "pincode": "263139"},
    {"state": "Uttarakhand", "city": "Roorkee", "pincode": "247667"},
    {"state": "Uttarakhand", "city": "Nainital", "pincode": "263001"},

    # West Bengal
    {"state": "West Bengal", "city": "Kolkata", "pincode": "700001"},
    {"state": "West Bengal", "city": "Howrah", "pincode": "711101"},
    {"state": "West Bengal", "city": "Siliguri", "pincode": "734001"},
    {"state": "West Bengal", "city": "Durgapur", "pincode": "713201"},
    {"state": "West Bengal", "city": "Asansol", "pincode": "713301"},

    # --- 8 Union Territories ---
    # Andaman and Nicobar Islands
    {"state": "Andaman and Nicobar Islands", "city": "Port Blair", "pincode": "744101"},

    # Chandigarh
    {"state": "Chandigarh", "city": "Chandigarh", "pincode": "160017"},

    # Dadra and Nagar Haveli and Daman and Diu
    {"state": "Dadra and Nagar Haveli and Daman and Diu", "city": "Daman", "pincode": "396210"},
    {"state": "Dadra and Nagar Haveli and Daman and Diu", "city": "Silvassa", "pincode": "396230"},
    {"state": "Dadra and Nagar Haveli and Daman and Diu", "city": "Diu", "pincode": "362520"},

    # Delhi
    {"state": "Delhi", "city": "New Delhi (Central)", "pincode": "110001"},
    {"state": "Delhi", "city": "North Delhi", "pincode": "110007"},
    {"state": "Delhi", "city": "South Delhi", "pincode": "110017"},
    {"state": "Delhi", "city": "East Delhi", "pincode": "110092"},

    # Jammu and Kashmir
    {"state": "Jammu and Kashmir", "city": "Srinagar", "pincode": "190001"},
    {"state": "Jammu and Kashmir", "city": "Jammu", "pincode": "180001"},
    {"state": "Jammu and Kashmir", "city": "Anantnag", "pincode": "192101"},

    # Ladakh
    {"state": "Ladakh", "city": "Leh", "pincode": "194101"},
    {"state": "Ladakh", "city": "Kargil", "pincode": "194103"},

    # Lakshadweep
    {"state": "Lakshadweep", "city": "Kavaratti", "pincode": "682555"},
    {"state": "Lakshadweep", "city": "Agatti", "pincode": "682553"},

    # Puducherry
    {"state": "Puducherry", "city": "Puducherry", "pincode": "605001"},
    {"state": "Puducherry", "city": "Karaikal", "pincode": "609602"}
]
