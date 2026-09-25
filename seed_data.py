"""
Prototype/demo data for PackWise AI.

IMPORTANT: These barrier, cost and sustainability ratings (1-5 scale) are
simplified, illustrative prototype values for demonstration purposes.
They are informed by general, widely published packaging-science
characteristics of each material (e.g. metallised/foil laminates having
very high oxygen & moisture barrier; glass being impermeable; PLA/PBAT
being compostable but a weaker moisture barrier). They are NOT sourced
from a specific lab test and should not be treated as experimentally
validated specifications. Use `data_status` to distinguish this.
"""

FOODS = [
    {"name": "Potato Chips / Savory Crisps", "category": "Snacks & Confectionery",
     "moisture": 5, "oxygen": 4, "light": 4, "fat": 5,
     "notes": "High lipid content, prone to staling and rancidity."},
    {"name": "Roasted Coffee Beans", "category": "Beverages",
     "moisture": 3, "oxygen": 5, "light": 3, "fat": 2,
     "notes": "Off-gasses CO2; oxygen exposure causes rapid flavor loss."},
    {"name": "Milk (Pasteurized)", "category": "Dairy & Meats",
     "moisture": 2, "oxygen": 3, "light": 5, "fat": 3,
     "notes": "Light exposure degrades riboflavin and causes off-flavors."},
    {"name": "Fresh Leafy Greens", "category": "Fresh Produce",
     "moisture": 4, "oxygen": 2, "light": 2, "fat": 1,
     "notes": "Needs breathable packaging to avoid condensation/rot; low barrier need."},
    {"name": "Biscuits / Cookies", "category": "Bakery & Cereals",
     "moisture": 4, "oxygen": 2, "light": 2, "fat": 3,
     "notes": "Moisture pickup causes loss of crunch."},
    {"name": "Tomato Sauce / Ketchup", "category": "Sauces & Condiments",
     "moisture": 1, "oxygen": 3, "light": 3, "fat": 1,
     "notes": "Acidic; needs chemically inert, heat-tolerant packaging for hot-fill."},
    {"name": "Breakfast Cereal Flakes", "category": "Bakery & Cereals",
     "moisture": 5, "oxygen": 2, "light": 1, "fat": 2,
     "notes": "Very hygroscopic; loses crispness quickly in humid air."},
    {"name": "Frozen Vegetables", "category": "Fresh Produce",
     "moisture": 3, "oxygen": 2, "light": 1, "fat": 1,
     "notes": "Needs freezer-durable film resistant to low-temperature cracking."},
    {"name": "Cooking Oil", "category": "Sauces & Condiments",
     "moisture": 1, "oxygen": 4, "light": 5, "fat": 5,
     "notes": "Oxidative rancidity accelerated strongly by light exposure."},
    {"name": "Cured Meat / Deli Slices", "category": "Dairy & Meats",
     "moisture": 3, "oxygen": 5, "light": 3, "fat": 4,
     "notes": "Needs strong oxygen barrier for vacuum/MAP packaging to prevent spoilage."},
]

# Preferred packaging "form factor" per food category — used as a mild,
# explainable adjustment so e.g. a rigid glass jar isn't recommended over a
# flexible pouch for a snack food. Not a hard filter, just a scoring nudge.
FOOD_CATEGORY_PREFERRED_FORMS = {
    "Snacks & Confectionery": ["flexible_film"],
    "Beverages": ["flexible_film", "rigid_container"],
    "Dairy & Meats": ["rigid_container", "flexible_film"],
    "Fresh Produce": ["flexible_film"],
    "Bakery & Cereals": ["flexible_film", "rigid_container"],
    "Sauces & Condiments": ["rigid_container"],
}

MATERIALS = [
    {
        "name": "PET / Aluminium Foil / PE Laminate",
        "short_code": "PET-AL-PE",
        "material_form": "flexible_film",
        "oxygen_barrier": 5, "moisture_barrier": 5, "light_barrier": 5,
        "grease_resistance": 5, "mechanical_strength": 4, "heat_resistance": 4,
        "cost_level": 4, "sustainability_level": 1,
        "recyclable": False, "compostable": False, "data_status": "prototype",
        "example_applications": "Snack & chips pouches, coffee bags, high-barrier flexible retort pouches",
        "advantages": [
            "Near-total oxygen, moisture and light barrier",
            "Excellent shelf-life extension for lipid-rich or oxygen-sensitive foods",
            "Good heat-seal integrity and puncture resistance",
        ],
        "limitations": [
            "Not recyclable in most municipal streams (multi-material laminate)",
            "Higher material cost than mono-material films",
            "Poor sustainability profile",
        ],
    },
    {
        "name": "Metallised BOPP Laminate",
        "short_code": "MET-BOPP",
        "material_form": "flexible_film",
        "oxygen_barrier": 4, "moisture_barrier": 4, "light_barrier": 5,
        "grease_resistance": 4, "mechanical_strength": 3, "heat_resistance": 3,
        "cost_level": 3, "sustainability_level": 2,
        "recyclable": False, "compostable": False, "data_status": "prototype",
        "example_applications": "Biscuit & cookie wrappers, confectionery bags, dry snack pouches",
        "advantages": [
            "Strong light and moderate oxygen/moisture barrier at lower cost than foil",
            "Good printability and shine for retail shelf appeal",
            "Lighter weight than aluminium foil laminate",
        ],
        "limitations": [
            "Barrier still lower than true aluminium foil laminate",
            "Multi-layer structure complicates recycling",
        ],
    },
    {
        "name": "Recyclable Mono-Material BOPP/CPP",
        "short_code": "MONO-BOPP",
        "material_form": "flexible_film",
        "oxygen_barrier": 3, "moisture_barrier": 3, "light_barrier": 2,
        "grease_resistance": 3, "mechanical_strength": 3, "heat_resistance": 3,
        "cost_level": 2, "sustainability_level": 4,
        "recyclable": True, "compostable": False, "data_status": "prototype",
        "example_applications": "Recyclable snack pouches, biscuit overwrap, dry bakery packaging",
        "advantages": [
            "Mono-polymer construction is widely recyclable in PP streams",
            "Moderate cost and decent moisture/oxygen performance",
            "Good mechanical toughness for form-fill-seal lines",
        ],
        "limitations": [
            "Lower oxygen/light barrier than foil or metallised options",
            "Not suitable for very high-fat, long-shelf-life products alone",
        ],
    },
    {
        "name": "Home-Compostable PLA/PBAT Film",
        "short_code": "PLA-PBAT",
        "material_form": "flexible_film",
        "oxygen_barrier": 2, "moisture_barrier": 2, "light_barrier": 1,
        "grease_resistance": 2, "mechanical_strength": 2, "heat_resistance": 1,
        "cost_level": 4, "sustainability_level": 5,
        "recyclable": False, "compostable": True, "data_status": "prototype",
        "example_applications": "Short-shelf-life snacks, fresh produce bags, compostable bakery wrap",
        "advantages": [
            "Home/industrially compostable — strong sustainability credentials",
            "Renewable, bio-based feedstock",
        ],
        "limitations": [
            "Weak oxygen and moisture barrier — unsuitable for long shelf life",
            "Poor heat resistance limits hot-fill or thermal sealing conditions",
            "Currently a higher-cost material at prototype scale",
        ],
    },
    {
        "name": "HDPE Rigid Bottle/Container",
        "short_code": "HDPE",
        "material_form": "rigid_container",
        "oxygen_barrier": 3, "moisture_barrier": 4, "light_barrier": 3,
        "grease_resistance": 3, "mechanical_strength": 5, "heat_resistance": 3,
        "cost_level": 2, "sustainability_level": 3,
        "recyclable": True, "compostable": False, "data_status": "prototype",
        "example_applications": "Milk bottles/jugs, yoghurt tubs, sauce and condiment containers",
        "advantages": [
            "Rigid, durable, widely recyclable (resin code 2)",
            "Good moisture barrier and low cost",
            "Well suited to liquid dairy and condiment products",
        ],
        "limitations": [
            "Moderate oxygen barrier only — may need additional liner for very O2-sensitive goods",
            "Bulkier than flexible film, higher transport footprint",
        ],
    },
    {
        "name": "PP Rigid Container / Tub",
        "short_code": "PP",
        "material_form": "rigid_container",
        "oxygen_barrier": 3, "moisture_barrier": 3, "light_barrier": 2,
        "grease_resistance": 4, "mechanical_strength": 4, "heat_resistance": 5,
        "cost_level": 2, "sustainability_level": 3,
        "recyclable": True, "compostable": False, "data_status": "prototype",
        "example_applications": "Deli tubs, microwaveable meal trays, cereal box liners",
        "advantages": [
            "Excellent heat resistance — microwave and hot-fill safe",
            "Good grease resistance for fatty foods",
            "Recyclable (resin code 5) in many regions",
        ],
        "limitations": [
            "Moderate barrier performance, not ideal as sole barrier for long shelf life",
            "Lower light barrier — needs opaque coloring for light-sensitive contents",
        ],
    },
    {
        "name": "Glass Jar / Bottle",
        "short_code": "GLASS",
        "material_form": "rigid_container",
        "oxygen_barrier": 5, "moisture_barrier": 5, "light_barrier": 3,
        "grease_resistance": 5, "mechanical_strength": 5, "heat_resistance": 5,
        "cost_level": 3, "sustainability_level": 4,
        "recyclable": True, "compostable": False, "data_status": "prototype",
        "example_applications": "Sauce and condiment jars, beverage bottles, preserves and pickles",
        "advantages": [
            "Total impermeability to oxygen and moisture — chemically inert",
            "Infinitely recyclable and reusable, strong consumer trust",
            "Excellent heat resistance for hot-fill and sterilization",
        ],
        "limitations": [
            "Heavy — higher transport carbon footprint and breakage risk",
            "Transparent glass needs UV-stabilised or tinted variant for light-sensitive contents",
        ],
    },
    {
        "name": "Coated Paperboard Carton",
        "short_code": "PAPERBOARD",
        "material_form": "rigid_container",
        "oxygen_barrier": 2, "moisture_barrier": 3, "light_barrier": 4,
        "grease_resistance": 2, "mechanical_strength": 3, "heat_resistance": 2,
        "cost_level": 2, "sustainability_level": 4,
        "recyclable": True, "compostable": True, "data_status": "prototype",
        "example_applications": "Cereal boxes, biscuit cartons, dry bakery secondary packaging",
        "advantages": [
            "Renewable fibre source, widely recyclable/compostable",
            "Good light barrier when printed/coated, low cost",
            "Lightweight, strong for shelf display and stacking",
        ],
        "limitations": [
            "Weak oxygen and grease barrier on its own — often needs an inner liner",
            "Not moisture-proof without additional coating",
        ],
    },
    {
        "name": "Vacuum-Skin EVOH Multilayer Film",
        "short_code": "EVOH-MULTI",
        "material_form": "flexible_film",
        "oxygen_barrier": 5, "moisture_barrier": 4, "light_barrier": 2,
        "grease_resistance": 4, "mechanical_strength": 4, "heat_resistance": 3,
        "cost_level": 5, "sustainability_level": 2,
        "recyclable": False, "compostable": False, "data_status": "prototype",
        "example_applications": "Vacuum-packed deli meats, cured meats, MAP-packed processed meat",
        "advantages": [
            "Very high oxygen barrier via EVOH layer — ideal for vacuum/MAP meat packaging",
            "Good clarity for retail visibility of product",
        ],
        "limitations": [
            "Multi-layer structure is difficult to recycle",
            "Highest cost tier material in this catalog",
        ],
    },
    {
        "name": "PVC/PVDC-Coated Cling Film",
        "short_code": "PVDC-FILM",
        "material_form": "flexible_film",
        "oxygen_barrier": 3, "moisture_barrier": 4, "light_barrier": 1,
        "grease_resistance": 3, "mechanical_strength": 2, "heat_resistance": 2,
        "cost_level": 2, "sustainability_level": 1,
        "recyclable": False, "compostable": False, "data_status": "prototype",
        "example_applications": "Fresh produce overwrap, short-term retail wrap for fresh greens",
        "advantages": [
            "Low cost, good clarity and cling for fresh produce display",
            "Breathable variants help prevent condensation on fresh greens",
        ],
        "limitations": [
            "Poor sustainability profile, generally not recyclable",
            "Weak light barrier and low mechanical strength",
        ],
    },
]
