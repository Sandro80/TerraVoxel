# =========================
# Configurazioni di Gioco
# =========================

# --- Spawn Alberi ---
ALBERI_ALTITUDINE = {
    "bassa": [
        {"model": "treeMinecraft.obj", "texture": "Leaves.001_color_low", "weight": 80},
        {"model": "tree.obj", "texture": "tree_base_color", "weight": 20}
    ],
    "media": [
        {"model": "treeMinecraft.obj", "texture": "Leaves.001_color_low", "weight": 80},
        {"model": "tree2.obj", "texture": "", "weight": 20}
    ],
    "alta": [
        {"model": "tree3.obj", "texture": "", "weight": 20},
        {"model": "tree.obj", "texture": "tree_base_color", "weight": 80}
    ]
}

# --- Spawn Animali ---
ANIMALI_ALTITUDINE = {
    "bassa": [
        {"model": "pig", "texture": "", "weight": 40, "suono_colpito": "pig_hit"},
        {"model": "sheep", "texture": "", "weight": 60, "suono_colpito": "sheep_hit"}
    ],
    "media": [
        {"model": "cow", "texture": "", "weight": 60, "suono_colpito": "cow_hit"},
        {"model": "sheep", "texture": "", "weight": 30, "suono_colpito": "sheep_hit"},
        {"model": "bull", "texture": "", "weight": 10, "suono_colpito": "cow_hit"}
    ],
    "alta": [
        {"model": "goat", "texture": "", "weight": 40, "suono_colpito": "goat_hit"},
        {"model": "deer", "texture": "", "weight": 60, "suono_colpito": "goat_hit"}
    ]
}

# --- Vegetazione ---
UV_MAP = {
    "azure_bluet": (0, 0),
    "bamboo": (1, 0),
    "beetroots": (2, 0),
    "dandelion": (3, 0),
    "deadbush": (4, 0),
    "fireflybush": (5, 0)
}

FLORA_ALTITUDINE = {
    "bassa": {"azure_bluet": 50, "beetroots": 20, "dandelion": 30},
    "media": {"dandelion": 50, "fireflybush": 30, "bamboo": 20},
    "alta": {"deadbush": 70, "fireflybush": 30}
}

# --- Terreni ---
TERRENI = {
    "pianura":  dict(octaves=1, seed=7,   noise_scale=60.0, height_multiplier=4),
    "colline":  dict(octaves=2, seed=123, noise_scale=50.0, height_multiplier=8),
    "montagne": dict(octaves=5, seed=99,  noise_scale=20.0, height_multiplier=16),
    "deserto":  dict(octaves=2, seed=17,  noise_scale=80.0, height_multiplier=2),
    "altopiano":dict(octaves=1, seed=88,  noise_scale=40.0, height_multiplier=6),
    "vulcanico":dict(octaves=4, seed=666, noise_scale=15.0, height_multiplier=20),
    "isole":    dict(octaves=3, seed=321, noise_scale=70.0, height_multiplier=10),
    "foresta":  dict(octaves=3, seed=101, noise_scale=45.0, height_multiplier=7),
    "palude":   dict(octaves=2, seed=404, noise_scale=55.0, height_multiplier=3),
    "crinale":  dict(octaves=6, seed=999, noise_scale=25.0, height_multiplier=18),
}
TIPO_TERRENO_DEFAULT = "montagne"

# --- Cubi ---
CUBI = [
    {'nome': 'Grass_Block', 'direzioni': {'front': (1, 0), 'back': (1, 0), 'left': (1, 0), 'right': (1, 0), 'top': (0, 0), 'bottom': (2, 0)}},
    {'nome': 'Dirt_Path_Block', 'direzioni': {'front': (5, 0), 'back': (5, 0), 'left': (5, 0), 'right': (5, 0), 'top': (6, 0), 'bottom': (2, 0)}},
    {'nome': 'Snowy_Grass_Block', 'direzioni': {'front': (4, 0), 'back': (4, 0), 'left': (4, 0), 'right': (4, 0), 'top': (3, 0), 'bottom': (2, 0)}},
    {'nome': 'Basalt_Block', 'direzioni': {'front': (14, 0), 'back': (14, 0), 'left': (14, 0), 'right': (14, 0), 'top': (14, 0), 'bottom': (14, 0)}},
    {'nome': 'Water_Block', 'direzioni': {'front': (6, 1), 'back': (6, 1), 'left': (6, 1), 'right': (6, 1), 'top': (6, 1), 'bottom': (6, 1)}},
    {'nome': 'Gold_Block', 'direzioni': {'front': (1, 1), 'back': (1, 1), 'left': (1, 1), 'right': (1, 1), 'top': (1, 1), 'bottom': (1, 1)}},
    {'nome': 'Bricks_Block', 'direzioni': {'front': (2, 1), 'back': (2, 1), 'left': (2, 1), 'right': (2, 1), 'top': (2, 1), 'bottom': (2, 1)}},
    {'nome': 'Barrel_Block', 'direzioni': {'front': (11, 0), 'back': (11, 0), 'left': (11, 0), 'right': (11, 0), 'top': (9, 0), 'bottom': (12, 0)}},
    {'nome': 'Bamboo_Block', 'direzioni': {'front': (8, 0), 'back': (8, 0), 'left': (8, 0), 'right': (8, 0), 'top': (7, 0), 'bottom': (7, 0)}}
]

# --- Audio ---
SUONI = {
    'place_block': 'assets/sounds/place.wav',
    'axe_miss': 'assets/sounds/axemiss.mp3',
    'axe_hit_tree': 'assets/sounds/axehittree.mp3',
    'pick_up_item': 'assets/sounds/pickupitem.mp3',
    'pop_item': 'assets/sounds/pop.mp3',
    'cow_hit': 'assets/sounds/cowhit.mp3',
    'sheep_hit': 'assets/sounds/sheephit.mp3',
    'goat_hit': 'assets/sounds/goathit.mp3',
    'pig_hit': 'assets/sounds/pighit.mp3',
    'footstep_grass': 'assets/sounds/footstep_grass.mp3',
    'footstep_snow': 'assets/sounds/footstep_snow.mp3',
    'footstep_water': 'assets/sounds/footstep_water.mp3',
    'footstep_dirt': 'assets/sounds/footstep_dirt.mp3'
}

MUSICA = {
    'background': {'file': 'assets/sounds/backgroundmusic.ogg', 'loop': True, 'volume': 0.4}
}
