import glob
from random import uniform
from ursina import *
from math import floor
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os
from perlin_noise import PerlinNoise
from ursina import Shader
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from animal import Animal
from audiomanager import AudioManager
from compass import Compass
from gamehud import GameHUD
from item import Item
from mappamondo import  Mappamondo
from minimap import MiniMap
from npc import NPC
from player import Player
from sky import SkyAmbient
from vegetation import Vegetazione
from tree import Tree
from vegetazioneChunk import VegetazioneChunk
from pathlib import Path
from PIL import Image
from collections import deque

from config_game import (
    ALBERI_ALTITUDINE, ANIMALI_ALTITUDINE, FLORA_ALTITUDINE, UV_MAP,
    TERRENI, TIPO_TERRENO_DEFAULT, CUBI, SUONI, MUSICA
)



"""terreni = {
    "pianura":     dict(octaves=1, seed=7,   noise_scale=60.0, height_multiplier=4),
    "colline":     dict(octaves=2, seed=123, noise_scale=50.0, height_multiplier=8),
    "montagne":    dict(octaves=5, seed=99,  noise_scale=20.0, height_multiplier=16),
    "deserto":     dict(octaves=2, seed=17, noise_scale=80.0, height_multiplier=2),
    "altopiano":   dict(octaves=1, seed=88, noise_scale=40.0, height_multiplier=6),
    "vulcanico":   dict(octaves=4, seed=666, noise_scale=15.0, height_multiplier=20),
    "isole":       dict(octaves=3, seed=321, noise_scale=70.0, height_multiplier=10),
    "foresta":     dict(octaves=3, seed=101, noise_scale=45.0, height_multiplier=7),
    "palude":      dict(octaves=2, seed=404, noise_scale=55.0, height_multiplier=3),
    "crinale":     dict(octaves=6, seed=999, noise_scale=25.0, height_multiplier=18),
}

tipo_terreno = "montagne"  # default
config = terreni.get(tipo_terreno, terreni["colline"])"""

# Esempio: terreno
tipo_terreno = TIPO_TERRENO_DEFAULT
config = TERRENI.get(tipo_terreno, TERRENI["colline"])

biome_noise = PerlinNoise(octaves=1, seed=999)  # Noise per decidere il tipo di bioma

app = Ursina()


def reset_world(chunk_folder, visited_file):
    # Cancella tutti i file .json dei chunk
    for file_path in glob.glob(os.path.join(chunk_folder, "*.json")):
        os.remove(file_path)
        print(f"🗑️ Eliminato: {file_path}")

    # Svuota il file delle coordinate visitate
    if os.path.exists(visited_file):
        with open(visited_file, "w") as f:
            json.dump([], f)
        print(f"📄 File coordinate visitate svuotato: {visited_file}")

    print("🌍 Mondo resettato con successo!\n")

def main_menu():
    print("=== MENU INIZIALE ===")
    print("1) Continua mondo esistente")
    print("2) Resetta e crea nuovo mondo")
    scelta = input("Scegli un'opzione (1/2): ").strip()

    if scelta == "2":
        reset_world("chunksaves", "chunks_visitati.json")
        # Qui puoi aggiungere la logica per generare il nuovo mondo
    elif scelta == "1":
        print("▶️ Continuo con il mondo esistente...\n")
        # Qui carichi il mondo esistente
    else:
        print("❌ Scelta non valida, riprova.\n")
        main_menu()


main_menu()




prev_count = 0
#window.fullscreen= True
free_camera = EditorCamera(enabled=False)

"""cubi = [{'nome': 'Grass_Block','direzioni': {'front': (1, 0),'back': (1, 0),'left': (1, 0),'right': (1, 0),'top': (0, 0),'bottom': (2, 0)}},
        {'nome': 'Dirt_Path_Block','direzioni': {'front': (5, 0),'back': (5, 0),'left': (5, 0),'right': (5, 0),'top': (6, 0),'bottom': (2, 0)}},
        {'nome': 'Snowy_Grass_Block','direzioni': {'front': (4, 0),'back': (4, 0),'left': (4, 0),'right': (4, 0),'top': (3, 0),'bottom': (2, 0)}} ,
        {'nome': 'Basalt_Block','direzioni': {'front': (14, 0),'back': (14, 0),'left': (14, 0),'right': (14, 0),'top': (14, 0),'bottom': (14, 0)}},
        {'nome': 'Water_Block','direzioni': {'front': (6, 1),'back': (6, 1),'left': (6, 1),'right': (6, 1),'top': (6, 1),'bottom': (6, 1)}},
        {'nome': 'Gold_Block','direzioni': {'front': (1, 1),'back': (1, 1),'left': (1, 1),'right': (1, 1),'top': (1, 1),'bottom': (1, 1)}},
        {'nome': 'Bricks_Block','direzioni': {'front': (2, 1),'back': (2, 1),'left': (2, 1),'right': (2, 1),'top': (2, 1),'bottom': (2, 1)}},
        {'nome': 'Barrel_Block','direzioni': {'front': (11, 0),'back': (11, 0),'left': (11, 0),'right': (11, 0),'top': (9, 0),'bottom': (12, 0)}},
        {'nome': 'Bamboo_Block','direzioni': {'front': (8, 0),'back': (8, 0),'left': (8, 0),'right': (8, 0),'top': (7, 0),'bottom': (7, 0)}}            
       ]"""

indice = 0
#blocco_selezionato = cubi[indice]
blocco_selezionato = CUBI[indice]


# Mostra il bottone  del blocco selezionato e il testo
bottone = Button(parent=camera.ui, model=Default, radius=0.1, origin=(0, 0), color=color.white, texture='assets/Grass_Block.png', collider='box', 
                 position = (0.72,-0.31),scale=(0.3, 0.3), enabled = False )
testo_blocco = Text(parent=camera.ui, origin=(0, 0),text=blocco_selezionato['nome'], position=(0.72, -0.45,-0.1), scale=1,enabled = False)

# Crea una luce direzionale con ombre
light = DirectionalLight()
light.look_at(Vec3(1, -1, -1))  # Direzione della luce
light.shadow_map_resolution = (1024,1024)
light.shadows = True            # Attiva le ombre
shadow_bounds = Entity(model='cube', scale=Vec3(50, 50, 50), visible=False)
light.update_bounds(shadow_bounds)
 

light_on = True
highligh_on = True
mini_map_on= True

world_map_show = False
mappa_mondo =  None

world_bounds = 30
total_chunks = (30 *2 + 1) * (30 *2 +1)   #asse x da -30 a + 30 . lo stesso per la z 
chunk_size = 16
atlas_size = (16,16)
render_distance = 1
MAX_render_distance = 5
BIOME_SCALE = 500.0  # Variabile globale
PERC_VEGETAZIONS_SPAWS = 0.02 #4%
PERC_TREES_SPAWS = 0.005     #2.5%
PERC_ROCKS_SPAWS = 0.005 
PERC_ANIMALS_SPAWS = 0.005    #1.5%

chunks_visitati = set()
chunks_esplorati = 1

modalita_creativa = False

chunk_generati_x_z = []

hud_attivo = True

sky = SkyAmbient(world_bounds,chunk_size)

"""# Carica effetti sonori
audio_manager = AudioManager()
audio_manager.load_sound('place_block', 'assets/sounds/place.wav')
audio_manager.load_sound('axe_miss', 'assets/sounds/axemiss.mp3')
audio_manager.load_sound('axe_hit_tree', 'assets/sounds/axehittree.mp3')
audio_manager.load_sound('pick_up_item', 'assets/sounds/pickupitem.mp3')
audio_manager.load_sound('pop_item', 'assets/sounds/pop.mp3')
#Animals
audio_manager.load_sound('cow_hit', 'assets/sounds/cowhit.mp3')
audio_manager.load_sound('sheep_hit', 'assets/sounds/sheephit.mp3')
audio_manager.load_sound('goat_hit', 'assets/sounds/goathit.mp3')
audio_manager.load_sound('pig_hit', 'assets/sounds/pighit.mp3')
#footsteps
audio_manager.load_sound('footstep_grass', 'assets/sounds/footstep_grass.mp3')
audio_manager.load_sound('footstep_snow', 'assets/sounds/footstep_snow.mp3')
audio_manager.load_sound('footstep_water', 'assets/sounds/footstep_water.mp3')
audio_manager.load_sound('footstep_dirt', 'assets/sounds/footstep_dirt.mp3')

audio_manager.play_music('assets/sounds/backgroundmusic.ogg', loop=True, volume=0.4)"""


# Esempio: audio
audio_manager = AudioManager()
for nome, path in SUONI.items():
    audio_manager.load_sound(nome, path)

bg = MUSICA['background']
audio_manager.play_music(bg['file'], loop=bg['loop'], volume=bg['volume'])

#------------------Items
apple = Item( position= (9,5,10), model='assets/models/items/apple-0.obj',texture = 'assets/models/items/apple-0.png', scale=1)
banana = Item( position= (12,5,4), model='assets/models/items/banana-0.obj',texture = 'assets/models/items/banana-0.png', scale=1)
cabbage = Item( position= (7,5,13), model='assets/models/items/cabbage-0.obj',texture = 'assets/models/items/cabbage-0.png', scale=1)

chest = Item( position= (9,4,9), model='assets/models/chest/chest.gltf', scale=1)

items_list = []
items_list.extend([apple, banana, cabbage,chest])
#----------------------------------------

mappa = Mappamondo() 
map_entity = None
map_file = None
MAPS_DIR = "maps"
os.makedirs(MAPS_DIR, exist_ok=True)
hud = GameHUD()
posP = Vec3(chunk_size / 2, 12, chunk_size / 2)
player = Player(hud,audio_manager,items_list,position=posP)
player.enabled = False  


compass = Compass(player_camera=camera,position= (-0.75, -0.4))
minimap = MiniMap(player, scan_interval=1.0)  # scansione ogni 1 secondo

npc = NPC(position= (6+0.5,7,6+0.5),model='assets/models/npc/npc.gltf', scale = 0.3,minimap=minimap,traceable= True)

previous_pos = Vec3(0,0,0)
last_step_time = 0  # globale
step_interval = 0.4  # secondi tra i passi

player_model = Entity(model='assets/square character.obj',scale=0.05, position=player.position + Vec3(0, -5, 0), visible=False)


selected_block_pos = None
selected_block_type = 0  # 0: erba, 1: muro

info_hud = Text(text='',origin=(-0.5, 0.5),position=(-0.85, 0.5),scale=1.25,background= False)

directions = {
    'front':  (0, 0, -1),
    'back':   (0, 0, 1),
    'left':   (-1, 0, 0),
    'right':  (1, 0, 0),
    'top':    (0, 1, 0),
    'bottom': (0, -1, 0),
}

def get_uv_coords(x, y, atlas_size = atlas_size):    
    step_x = 1 / atlas_size[0]
    step_y = 1 / atlas_size[1]
    u = x * step_x
    #v = y * step_y
    v = 1 - (y + 1) * step_y  # 👈 Inversione Y
    return [
        Vec2(u, v),
        Vec2(u + step_x, v),
        Vec2(u + step_x, v + step_y),
        Vec2(u, v + step_y)
    ]

def add_face(vertices, triangles, uvs, position, direction, index_offset, block_type):
    x, y, z = position

    face_data = {
        'front':  [(0,0,0), (1,0,0), (1,1,0), (0,1,0)],
        'back':   [(1,0,1), (0,0,1), (0,1,1), (1,1,1)],
        'left':   [(0,0,1), (0,0,0), (0,1,0), (0,1,1)],
        'right':  [(1,0,0), (1,0,1), (1,1,1), (1,1,0)],
        'top':    [(0,1,0), (1,1,0), (1,1,1), (0,1,1)],
        'bottom': [(0,0,1), (1,0,1), (1,0,0), (0,0,0)],
    }

    face_vertices = [Vec3(x+vx, y+vy, z+vz) for vx, vy, vz in face_data[direction]]
    vertices.extend(face_vertices)

    triangles.extend([
        index_offset, index_offset+1, index_offset+2,
        index_offset, index_offset+2, index_offset+3
    ])

    #blocco_corrente = cubi[block_type]
    blocco_corrente = CUBI[block_type]
    if direction in blocco_corrente['direzioni']:
        x, y = blocco_corrente['direzioni'][direction]
        face_uvs = get_uv_coords(x, y)
    else:
        # Se la direzione non è definita, puoi usare una texture di default
        face_uvs = get_uv_coords(0, 0)          

    uvs.extend(face_uvs)

class Chunk(Entity):
    #def __init__(self, origin=(0, 0, 0)):
    def __init__(self, origin=(0, 0, 0), octaves=3, seed=42, noise_scale=30.0, height_multiplier=12, generate=True):
        super().__init__()
        self.origin = origin
        self.blocks = {}
        self.vertices = []
        self.triangles = []
        self.uvs = []
        self.index_offset = 0
        self.texture = load_texture('assets/atlasMinecraft.png')
        self.texture_normal = load_texture('assets/atlasMinecraftNormal.png')
        self.chunk_size = chunk_size


        self.octaves =octaves
        self.seed = seed
        #self.noise = PerlinNoise(octaves=3, seed=42)  # 👈 Noise 2D
        self.noise = PerlinNoise(octaves=octaves, seed=seed)
        self.noise_scale = noise_scale
        #print("DEBUG: self.noise_scale =", self.noise_scale, "tipo:", type(self.noise_scale))
        self.height_multiplier = height_multiplier
        #da testare
        self.minimap_render = True

        self.shader=lit_with_shadows_shader
        self.timer_check_coliders = 0
        self.interval_check_colliders = 0.75

        self.modified = False

         # Calcolo heightmap subito
        self.heightmap = self.generate_heightmap()

        self.vegetazioni_chunk = []

        #self.vegetazione = []
        self.alberi =[]
        self.animali = []
        self.chunk_veg = Entity()
         
        self.generate_blocks()       
        self.build_mesh()

        if generate:
            print("Generazione saltata")
           
            #self.spawn_alberi()
            self.spawn_vegetazione()
            #self.spawn_animali()

            self.spawn_entities()
            

    def generate_heightmap(self):
        heightmap = [[0 for _ in range(chunk_size)] for _ in range(chunk_size)]
        for x in range(chunk_size):
            for z in range(chunk_size):
                world_x = self.origin[0] + x
                world_z = self.origin[2] + z
                h = int(
                    self.noise([world_x / self.noise_scale, world_z / self.noise_scale])
                    * self.height_multiplier
                    + chunk_size / 2
                )
                heightmap[x][z] = h
        return heightmap

    def unload(self):
        # Distruggi alberi
        for albero in list(self.alberi):
            if albero.minimap and albero in albero.minimap.tracked:
                albero.minimap.tracked.remove(albero)
            destroy(albero)
        self.alberi.clear()

        # Rimuovi e distruggi tutti gli animali
        for animale in list(self.animali):
            if animale.minimap and animale in animale.minimap.tracked:
                animale.minimap.tracked.remove(animale)
            destroy(animale)
        self.animali.clear()

        # Distruggi vegetazione
        if hasattr(self, "chunk_veg") and self.chunk_veg:
            destroy(self.chunk_veg)
            self.chunk_veg = None

        # Svuota la lista per evitare accumuli di dati
        self.vegetazioni_chunk = []


        # Distruggi eventuali entità orfane legate al chunk
        for e in scene.entities:
            if getattr(e, "parent", None) == self:
                destroy(e)

    def save(self):
        print(f"Chunk {self.origin} saved.")
        ox, oy, oz = map(int, self.origin)

        def vec3_to_list(v):
            return [float(v.x), float(v.y), float(v.z)]

        return {
            'origin': vec3_to_list(self.origin),
            'octaves': self.octaves,
            'seed': self.seed,
            'noise_scale': self.noise_scale,
            'height_multiplier': self.height_multiplier,
            'alberi': [
                {
                    'model': Path(a.model.name).stem,
                    'texture': a.texture.name if a.texture else None,
                    # posizione relativa al chunk
                    'position': [
                        a.x - ox,
                        a.y - oy,
                        a.z - oz
                    ],
                    'rotation': vec3_to_list(a.rotation),
                    'scale': vec3_to_list(a.scale)
                } for a in self.alberi
            ],
            'animali': [
                {
                    'nome': getattr(a, 'nome', ''),
                    'model': Path(a.model.name).stem,
                    'texture': Path(a.texture.name).stem if a.texture else None,
                    'position': [
                        a.x - ox,
                        a.y - oy,
                        a.z - oz
                    ],
                    'rotation': vec3_to_list(a.rotation),
                    'scale': [a.scale.x, a.scale.y, a.scale.z],
                    'salute': getattr(a, 'salute', 100),
                    'suono_colpito': getattr(a, 'suono_colpito', None),
                    'exp': getattr(a, 'exp', 10),
                    'movement_cellsxz': getattr(a, 'movement_cellsxz', [])
                } for a in self.animali
            ],
            'vegetazione': [
                {
                    'posizione': (
                        veg[0][0],
                        veg[0][1],
                        veg[0][2]
                    ),  # già relativa
                    'uv_coords': veg[1],
                    'doppio': veg[2]
                } for veg in self.vegetazioni_chunk
            ]
        }


    @staticmethod
    def load(data):
        chunk = Chunk(
            origin=list_to_vec3(data['origin']),
            octaves=data['octaves'],
            seed=data['seed'],
            noise_scale=data['noise_scale'],
            height_multiplier=data['height_multiplier'],
            generate=False
        )

        ox, oy, oz = chunk.origin

        # Carica alberi
        for a in data['alberi']:
            pos = Vec3(
                a['position'][0] + ox,
                a['position'][1] + oy,
                a['position'][2] + oz
            )
            albero = Tree(
                audio_manager=audio_manager,
                model_name=a['model'],
                texture_model=a['texture'],
                position=pos,
                scale=list_to_vec3(a['scale']),
                minimap=minimap
            )
            albero.rotation = list_to_vec3(a['rotation'])
            albero.parent = chunk
            chunk.alberi.append(albero)

        # Carica animali
        for a in data['animali']:
            pos = Vec3(
                a['position'][0] + ox,
                a['position'][1] + oy,
                a['position'][2] + oz
            )
            scale = list_to_vec3(a['scale'])
            if scale == Vec3(0, 0, 0):
                scale = Vec3(0.9, 0.9, 0.9)

            animale = Animal(
                nome=a.get('nome', 'Sconosciuto'),
                audio_manager=audio_manager,
                model_name=a['model'],
                texture_model=a['texture'],
                posizione=pos,
                salute=a.get('salute', 100),
                suono_colpito=a.get('suono_colpito', None),
                minimap=minimap,
                traceable=True,
                exp=a.get('exp', 10),
                rotation=list_to_vec3(a['rotation']),
                scale=scale,
                parent=chunk
            )

            # 🔹 Calcola l'altezza del terreno nella posizione dell'animale
            altezza = chunk.get_terrain_height(pos.x, pos.z)  # <-- usa la tua funzione di altezza

            # 🔹 Rigenera le celle di movimento
            animale.movement_cellsxz = chunk.generate_animal_movement_cells(animale, altezza)

            chunk.animali.append(animale)

        # Caricamento vegetazione (FIX: niente offset extra)
        vegetazioni_data = data.get('vegetazione', [])

        # 1️⃣ Distruggi eventuale vegetazione precedente
        if hasattr(chunk, "chunk_veg") and chunk.chunk_veg:
            destroy(chunk.chunk_veg)
            chunk.chunk_veg = None

        # 2️⃣ Svuota la lista prima di riempirla
        chunk.vegetazioni_chunk = []

        vegetazioni_rel = [
            (tuple(veg['posizione']), veg['uv_coords'], veg['doppio'])
            for veg in vegetazioni_data
        ]
        chunk.chunk_veg = VegetazioneChunk(
            posizione=(0, 0, 0),  # <-- qui il fix: niente chunk.origin
            vegetazioni=vegetazioni_rel
        )
        chunk.chunk_veg.parent = chunk
        chunk.vegetazioni_chunk = vegetazioni_rel
        

        return chunk

    def update(self):
        if not self.enabled:
            return  # ❌ Chunk non attivo, salta tutto
     
        # 1️⃣ Muove animali sempre
        for animale in self.animali:
            animale.muovi(time.dt)

        # 2️⃣ Timer per controllare collider → solo ogni intervallo
        self.timer_check_coliders += time.dt
        if self.timer_check_coliders < self.interval_check_colliders:
            return
        self.timer_check_coliders = 0  # reset timer

  
        # 3️⃣ Controllo animali e alberi con soglie diverse
        self.controlla_collider(self.animali, 10)  # animali entro 10 unità
        self.controlla_collider(self.alberi, 10)   # alberi entro 15 unità

       

    # 3️⃣ Funzione interna per controllare un gruppo di entità
    def controlla_collider(self,entita_lista, soglia):
        for ent in entita_lista:
            distanza = (ent.position - player.position).length()
            if distanza < soglia:
                ent.collider = 'box'
                if isinstance(ent,Tree):
                    ent.reset_collider()
                #ent.color = color.red
            else:
                ent.collider = None
                #ent.color = color.green

    def get_terrain_height(self, world_x, world_z):
        height = int(self.noise([world_x / self.noise_scale, world_z / self.noise_scale]) * self.height_multiplier + chunk_size / 2)
        return self.origin[1] + height

    def get_terrain_height_new(self, x, z):
        # Coordinate locali nel chunk
        lx = int(x - self.origin[0])
        lz = int(z - self.origin[2])
        if 0 <= lx < chunk_size and 0 <= lz < chunk_size:
            return self.heightmap[lx][lz]
        else:
            # Se fuori dal chunk, calcola al volo o gestisci diversamente
            return int(
                self.noise([x / self.noise_scale, z / self.noise_scale])
                * self.height_multiplier
                + chunk_size / 2)

    def spawn_vegetazione(self):
        # 1️⃣ Distruggi eventuale vegetazione precedente
        if hasattr(self, "chunk_veg") and self.chunk_veg:
            destroy(self.chunk_veg)
            self.chunk_veg = None

        # 2️⃣ Svuota la lista PRIMA di riempirla
        self.vegetazioni_chunk = []


        uv_map = {
            "azure_bluet": (0, 0), "bamboo": (1, 0), "beetroots": (2, 0),
            "dandelion": (3, 0), "deadbush": (4, 0), "fireflybush": (5, 0)
        }

        flora_altitudine = {
            "bassa": {"azure_bluet": 50, "beetroots": 20, "dandelion": 30},
            "media": {"dandelion": 50, "fireflybush": 30, "bamboo": 20},
            "alta": {"deadbush": 70, "fireflybush": 30}
        }

        for x in range(chunk_size):
            for z in range(chunk_size):
                world_x = self.origin[0] + x
                world_z = self.origin[2] + z

                height = int(self.noise([world_x / self.noise_scale, world_z / self.noise_scale]) * self.height_multiplier + chunk_size / 2)
                world_y = self.origin[1] + height

                if height < 5:
                    flora = flora_altitudine["bassa"]
                elif 5 <= height < 10:
                    flora = flora_altitudine["media"]
                elif 10 <= height < 25:
                    flora = flora_altitudine["alta"]
                else:
                    continue

                fiori, pesi = normalizza_pesi(flora)
                tipo = random.choices(fiori, weights=pesi)[0]

                if random.random() < PERC_VEGETAZIONS_SPAWS:
                    if any(tree.position.x == world_x + 0.5 and tree.position.z == world_z + 0.5 for tree in self.alberi):
                        continue
                    self.vegetazioni_chunk.append(((world_x + 0.5, world_y + 1.5, world_z + 0.5), uv_map[tipo], True))

        self.chunk_veg = VegetazioneChunk(posizione=(0,0,0), vegetazioni=self.vegetazioni_chunk)
        self.chunk_veg.parent = self

    

    def spawn_alberi(self):
        alberi_altitudine = {
                                "bassa": [{"model" : "treeMinecraft.obj", "texture": "Leaves.001_color_low", "weight": 80},
                                          {"model" : "tree.obj", "texture": "tree_base_color", "weight": 20}],
                                "media": [{"model" : "treeMinecraft.obj", "texture": "Leaves.001_color_low", "weight": 80},
                                          {"model" : "tree2.obj", "texture": "", "weight": 20}],
                                "alta":  [{"model" : "tree3.obj", "texture": "", "weight": 20},
                                          {"model" : "tree.obj", "texture": "tree_base_color", "weight": 80}]
                            }


        for x in range(chunk_size):
            for z in range(chunk_size):
                world_x = self.origin[0] + x
                world_z = self.origin[2] + z

                # Ricalcola l'altezza come nel generate_blocks
                height = int(self.noise([world_x / self.noise_scale, world_z / self.noise_scale]) * self.height_multiplier + chunk_size / 2)
                world_y = self.origin[1] + height
                pos = (world_x, world_y, world_z)
             
                # Decidi tipo vegetazione in base all'altezza
                f = 0
                if height < 6:
                    f = 'bassa'
                elif 6 <= height < 11:
                    f = 'media'
                else:
                    f = 'alta'

                # Probabilità di spawn
                if random.random() < PERC_TREES_SPAWS:   
                    fascia = f
                    opzioni = alberi_altitudine[fascia]
                    pesi = [item['weight'] for item in opzioni]
                    tipo_albero = random.choices(opzioni, weights=pesi)[0]
                    tree = Tree(audio_manager,model_name=tipo_albero['model'].replace('.obj', ''),
                                texture_model=tipo_albero['texture'].replace('.png', '') if tipo_albero['texture'] else None,
                                position=(world_x + 0.5, world_y + 1, world_z + 0.5),
                                scale= 1, minimap=minimap
                                )

                    tree.parent = self
                    self.alberi.append(tree)

    def spawn_animali(self):
        animali_altitudine = {
                                "bassa": [{"model" : "pig", "texture": "", "weight": 40, "suono_colpito": "pig_hit"},
                                          {"model" : "sheep", "texture": "", "weight": 60, "suono_colpito": "sheep_hit"}],
                                "media": [{"model" : "cow", "texture": "", "weight": 60, "suono_colpito": "cow_hit"},
                                          {"model" : "sheep", "texture": "", "weight": 30, "suono_colpito": "sheep_hit"},
                                          {"model" : "bull", "texture": "", "weight": 10, "suono_colpito": "cow_hit"}],
                                "alta":  [{"model" : "goat", "texture": "", "weight": 40, "suono_colpito": "goat_hit"},
                                          {"model" : "deer", "texture": "", "weight": 60, "suono_colpito": "goat_hit"}]
                            }


        for x in range(chunk_size):
            for z in range(chunk_size):
                world_x = self.origin[0] + x
                world_z = self.origin[2] + z

                # Ricalcola l'altezza come nel generate_blocks
                height = int(self.noise([world_x / self.noise_scale, world_z / self.noise_scale]) * self.height_multiplier + chunk_size / 2)
                world_y = self.origin[1] + height
                pos = (world_x, world_y, world_z)
             
                # Decidi tipo vegetazione in base all'altezza
                f = 0
                if height < 6:
                    f = 'bassa'
                elif 6 <= height < 10:
                    f = 'media'
                else:
                    f = 'alta'

                # Probabilità di spawn
                if random.random() < PERC_ANIMALS_SPAWS:   
                    if any(tree.position.x == world_x + 0.5 and tree.position.z == world_z + 0.5 for tree in self.alberi):
                        #print(f"Albero presente! x= {world_x} z= {world_z}")
                        continue  # Salta  l'animale se c'è un albero         
                    fascia = f
                    opzioni = animali_altitudine[fascia]
                    pesi = [item['weight'] for item in opzioni]
                    tipo_animale = random.choices(opzioni, weights=pesi)[0]
                    
                    animal = Animal(nome =tipo_animale['model'].capitalize(),audio_manager= audio_manager,model_name= tipo_animale['model'].replace('.gltf', ''),
                                    texture_model = tipo_animale['texture'].replace('.png', ''),
                                    posizione=(world_x + 0.5, world_y + 1, world_z + 0.5), salute =100, suono_colpito=tipo_animale['suono_colpito'], minimap = minimap,
                                    traceable= True)
                    animal.scale =0.9
                    
                    
                    animal.movement_cellsxz  = self.generate_animal_movement_cells(animal,world_y)

                    animal.parent = self                    
                    self.animali.append(animal)


    def generate_animal_movement_cells(self, animale, height):
        """
        Restituisce tutte le celle raggiungibili alla stessa altezza di spawn dell'animale,
        evitando alberi e dislivelli.
        """
        visited = set()
        movement_cells = []
        queue = deque()

        # Coordinate di partenza (convertite in int)
        start_x = int(animale.position.x)
        start_z = int(animale.position.z)

        queue.append((start_x, start_z))
        visited.add((start_x, start_z))

        # Direzioni di movimento (4-neighbors)
        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        while queue:
            cx, cz = queue.popleft()

            # Aggiungi cella alla lista
            movement_cells.append((cx, cz))

            for dx, dz in directions:
                nx, nz = cx + dx, cz + dz

                # Evita di uscire dal chunk
                if not (self.origin[0] <= nx < self.origin[0] + chunk_size and
                        self.origin[2] <= nz < self.origin[2] + chunk_size):
                    continue

                if (nx, nz) in visited:
                    continue

                # Altezza del blocco
                block_height = self.get_terrain_height(nx, nz)

                # Controlla se è alla stessa quota
                if block_height != height:
                    continue

                # Evita celle con alberi
                if any(tree.position.x == nx + 0.5 and tree.position.z == nz + 0.5 for tree in self.alberi):
                    continue

                visited.add((nx, nz))
                queue.append((nx, nz))

        return movement_cells


    def spawn_entities(self):
        # Pulizia vegetazione precedente
        if hasattr(self, "chunk_veg") and self.chunk_veg:
            destroy(self.chunk_veg)
            self.chunk_veg = None
        self.vegetazioni_chunk = []

        # Set per posizioni occupate da alberi
        posizioni_alberi = set()

        # Unico ciclo di spawn usando la heightmap già calcolata in self.heightmap
        for x in range(chunk_size):
            for z in range(chunk_size):
                height = self.heightmap[x][z]  # <-- lettura diretta
                world_x = self.origin[0] + x
                world_z = self.origin[2] + z
                world_y = self.origin[1] + height

                # Fasce separate
                # Alberi
                if height < 6:
                    fascia_alberi = 'bassa'
                elif 6 <= height < 11:
                    fascia_alberi = 'media'
                else:
                    fascia_alberi = 'alta'

                # Animali
                if height < 6:
                    fascia_animali = 'bassa'
                elif 6 <= height < 10:
                    fascia_animali = 'media'
                else:
                    fascia_animali = 'alta'

                # Vegetazione
                if height < 5:
                    fascia_flora = 'bassa'
                elif 5 <= height < 10:
                    fascia_flora = 'media'
                elif 10 <= height < 25:
                    fascia_flora = 'alta'
                else:
                    fascia_flora = None

                # Spawn Alberi
                if random.random() < PERC_TREES_SPAWS:
                    opzioni = ALBERI_ALTITUDINE[fascia_alberi]
                    pesi = [item['weight'] for item in opzioni]
                    tipo_albero = random.choices(opzioni, weights=pesi)[0]

                    tree = Tree(
                        audio_manager,
                        model_name=tipo_albero['model'].replace('.obj', ''),
                        texture_model=tipo_albero['texture'].replace('.png', '') if tipo_albero['texture'] else None,
                        position=(world_x + 0.5, world_y + 1, world_z + 0.5),
                        scale=1,
                        minimap=minimap
                    )
                    tree.parent = self
                    self.alberi.append(tree)
                    posizioni_alberi.add((world_x + 0.5, world_z + 0.5))

                # Spawn Animali (solo se non c'è un albero)
                if random.random() < PERC_ANIMALS_SPAWS and (world_x + 0.5, world_z + 0.5) not in posizioni_alberi:
                    opzioni = ANIMALI_ALTITUDINE[fascia_animali]
                    pesi = [item['weight'] for item in opzioni]
                    tipo_animale = random.choices(opzioni, weights=pesi)[0]

                    animal = Animal(
                        nome=tipo_animale['model'].capitalize(),
                        audio_manager=audio_manager,
                        model_name=tipo_animale['model'].replace('.gltf', ''),
                        texture_model=tipo_animale['texture'].replace('.png', ''),
                        posizione=(world_x + 0.5, world_y + 1, world_z + 0.5),
                        salute=100,
                        suono_colpito=tipo_animale['suono_colpito'],
                        minimap=minimap,
                        traceable=True
                    )
                    animal.scale = 0.9
                    animal.movement_cellsxz = self.generate_animal_movement_cells(animal, world_y)
                    animal.parent = self
                    self.animali.append(animal)

                # Spawn Vegetazione (solo se non c'è un albero)
                if fascia_flora and random.random() < PERC_VEGETAZIONS_SPAWS and (world_x + 0.5, world_z + 0.5) not in posizioni_alberi:
                    flora = FLORA_ALTITUDINE[fascia_flora]
                    fiori, pesi = normalizza_pesi(flora)
                    tipo = random.choices(fiori, weights=pesi)[0]
                    self.vegetazioni_chunk.append(
                        ((world_x + 0.5, world_y + 1.5, world_z + 0.5), UV_MAP[tipo], True)
                    )

        # Crea chunk vegetazione
        self.chunk_veg = VegetazioneChunk(posizione=(0, 0, 0), vegetazioni=self.vegetazioni_chunk)
        self.chunk_veg.parent = self



    def generate_blocks(self):
       
        for x in range(chunk_size):
            for z in range(chunk_size):
                world_x = self.origin[0] + x
                world_z = self.origin[2] + z
 
                height = int(self.noise([world_x / self.noise_scale, world_z / self.noise_scale]) * self.height_multiplier + chunk_size / 2)

                for y in range(chunk_size):
                    world_y = self.origin[1] + y
                    pos = (world_x, world_y, world_z)

                    # Genera blocchi fino all'altezza
                    self.blocks[pos] = 0 if y <= height else None

                    if y <3: self.blocks[pos] = 4 
                    if y >=3 and y<=7: self.blocks[pos] = 0 
                    if y >7 and y <=9: self.blocks[pos] = 1
                    if y >9 and y <= height: self.blocks[pos] = 2
                    if y>height: self.blocks[pos] = None 
                                     

    def build_mesh(self):
        self.vertices.clear()
        self.triangles.clear()
        self.uvs.clear()
        self.index_offset = 0

        for pos in self.blocks:
            block_type = self.blocks[pos]
            if block_type is None:
                continue
            for dir_name, offset in directions.items():
                neighbor = (pos[0]+offset[0], pos[1]+offset[1], pos[2]+offset[2])
                if self.blocks.get(neighbor) is None:
                    add_face(self.vertices, self.triangles, self.uvs, pos, dir_name, self.index_offset, block_type)
                    self.index_offset += 4

        self.model = Mesh(vertices=self.vertices, triangles=self.triangles, uvs=self.uvs, mode='triangle')      
        self.collider = self.model

    def remove_block(self, pos):
        if self.blocks.get(pos) is not None:
            self.blocks[pos] = None
            self.build_mesh()

def vec3_to_list(v):
    return [int(v.x), int(v.y), int(v.z)]

def list_to_vec3(lst):
    return Vec3(int(lst[0]), int(lst[1]), int(lst[2]))

# 🔧 Funzione esterna per salvare su file
def save_chunk_to_file(chunk):
    origin = chunk.origin
    ox, oy, oz = map(int, origin)  # così ti assicuri che siano interi
    filename = f"chunksaves/chunk_({ox},{oy},{oz}).json"
    with open(filename, 'w') as f:
        json.dump(chunk.save(), f, indent=4)

def load_chunk_from_file(origin):
    ox, oy, oz = map(int, origin)  # così ti assicuri che siano interi
    filename = f"chunksaves/chunk_({ox},{oy},{oz}).json"
    with open(filename, 'r') as f:
        data = json.load(f)
    return Chunk.load(data)

def normalizza_pesi(percentuali_dict):
    fiori = list(percentuali_dict.keys())
    percentuali = list(percentuali_dict.values())
    totale = sum(percentuali)
    pesi_normalizzati = [p / totale for p in percentuali]
    return fiori, pesi_normalizzati

def get_chunk_coords(position):
    return (floor(position.x / chunk_size), floor(position.z / chunk_size))


def get_biome_type(x, z):
    value = biome_noise([x / BIOME_SCALE, z / BIOME_SCALE])  # Scala ampia per transizioni morbide

    #original
    if value < 0.2:
        return "isole"
    elif value < 0.4:
        return "colline"
    elif value < 0.6:
        return "montagne"
    elif value < 0.8:
        return "crinale"
    else:
        return "foresta"
    
def is_chunk_in_front(chunk):
    camera_forward = camera.forward.normalized()
    to_chunk = (chunk.origin - camera.world_position).normalized()
    dot = camera_forward.dot(to_chunk)
    return dot > 0.3  # Puoi regolare la soglia: più alto = più stretta la visione


# Code separate
chunk_load_queue = []
chunk_generation_queue = []
chunk_save_queue = []
chunk_destroy_queue = []

def update_chunks():
    global chunks, chunk_load_queue, chunk_generation_queue, chunk_save_queue, chunk_destroy_queue

    player_chunk_x = int(player.position[0] // chunk_size)
    player_chunk_z = int(player.position[2] // chunk_size)

    active_chunks = set()

    # Calcola i chunk da mantenere attivi
    for dx in range(-render_distance, render_distance + 1):
        for dz in range(-render_distance, render_distance + 1):
            chunk_x = player_chunk_x + dx
            chunk_z = player_chunk_z + dz

            if not (-world_bounds <= chunk_x <= world_bounds and -world_bounds <= chunk_z <= world_bounds):
                continue

            chunk_coords = (chunk_x, chunk_z)
            active_chunks.add(chunk_coords)

            if chunk_coords not in chunks:
                filename = f"chunksaves/chunk_({chunk_x*chunk_size},0,{chunk_z*chunk_size}).json"

                if os.path.exists(filename):
                    # Metto in coda il caricamento
                    chunk_load_queue.append((chunk_coords, filename))
                else:
                    # Metto in coda la generazione
                    chunk_generation_queue.append(chunk_coords)
            else:
                chunks[chunk_coords].enable()

    # Chunk fuori distanza → metto in coda salvataggio/distruzione
    for coords in list(chunks.keys()):
        if coords not in active_chunks:
            if chunks[coords].modified:
                chunk_save_queue.append(coords)
            else:
                chunk_destroy_queue.append(coords)

def process_chunk_queues():
    global chunks

    # 1️⃣ Caricamento
    if chunk_load_queue:
        coords = chunk_load_queue.pop(0)
        # Se la coda di load contiene tuple (coords, filename), estrai coords
        if isinstance(coords, tuple) and len(coords) == 2 and not isinstance(coords[0], int):
            coords, filename = coords
        else:
            filename = None

        if coords in chunks:
            print(f"ℹ️ Chunk già presente, skip: {coords}")
            return

        chunk_x, chunk_z = coords
        chunk_data = load_chunk_from_file((chunk_x * chunk_size, 0, chunk_z * chunk_size))
        if chunk_data:
            chunks[coords] = chunk_data
            chunks[coords].enable()
            print(f"📂 Chunk caricato: {coords}")
        else:
            print(f"⚠️ File non trovato per {coords}, passo a generazione...")
            # Controllo anti-duplicato robusto
            if all(c != coords for c in chunk_load_queue) and coords not in chunk_generation_queue:
                chunk_generation_queue.append(coords)
                print(f"📥 Aggiunto a coda generazione: {coords}")
            else:
                print(f"ℹ️ Chunk già in coda, skip enqueue: {coords}")
        return  # una operazione per frame

    # 2️⃣ Generazione
    if chunk_generation_queue:
        chunk_coords = chunk_generation_queue.pop(0)
        if chunk_coords in chunks:
            print(f"ℹ️ Chunk già presente, skip: {chunk_coords}")
            return
        chunk_x, chunk_z = chunk_coords
        origin = (chunk_x * chunk_size, 0, chunk_z * chunk_size)
        biome = get_biome_type(origin[0], origin[2])
        #config = terreni.get(biome, terreni["colline"])
        config = TERRENI.get(biome, TERRENI["colline"])
        new_chunk = Chunk(origin=origin, **config)
        chunks[chunk_coords] = new_chunk
        save_chunk_to_file(new_chunk)
        print(f"✅ Chunk generato e salvato: {chunk_coords}")
        return

    # 3️⃣ Salvataggio
    if chunk_save_queue:
        coords = chunk_save_queue.pop(0)
        if coords in chunks:
            save_chunk_to_file(chunks[coords])
            if coords not in chunk_destroy_queue:
                chunk_destroy_queue.append(coords)
            print(f"💾 Chunk salvato: {coords}")
        else:
            print(f"⚠️ Salvataggio fallito, chunk inesistente: {coords}")
        return

    # 4️⃣ Distruzione
    if chunk_destroy_queue:
        coords = chunk_destroy_queue.pop(0)
        if coords in chunks:
            chunks[coords].unload()
            destroy(chunks[coords])
            del chunks[coords]
            print(f"🗑️ Chunk distrutto: {coords}")
        else:
            print(f"⚠️ Distruzione fallita, chunk inesistente: {coords}")
        return


def process_chunk_queuesold():
    global chunks

    # 1️⃣ Caricamento
    if chunk_load_queue:
        coords, filename = chunk_load_queue.pop(0)
        chunk_x, chunk_z = coords
        chunks[coords] = load_chunk_from_file((chunk_x*chunk_size, 0, chunk_z*chunk_size))
        chunks[coords].enable()
        print(f"📂 Chunk caricato: {coords}")
        return  # una operazione per frame

    # 2️⃣ Generazione
    if chunk_generation_queue:
        chunk_coords = chunk_generation_queue.pop(0)
        chunk_x, chunk_z = chunk_coords
        origin = (chunk_x * chunk_size, 0, chunk_z * chunk_size)
        biome = get_biome_type(origin[0], origin[2])
        #config = terreni.get(biome, terreni["colline"])
        config = TERRENI.get(biome, TERRENI["colline"])
        new_chunk = Chunk(origin=origin, **config)
        chunks[chunk_coords] = new_chunk
        save_chunk_to_file(new_chunk)
        print(f"✅ Chunk generato e salvato: {chunk_coords}")
        return

    # 3️⃣ Salvataggio
    if chunk_save_queue:
        coords = chunk_save_queue.pop(0)
        save_chunk_to_file(chunks[coords])
        chunk_destroy_queue.append(coords)
        print(f"💾 Chunk salvato: {coords}")
        return

    # 4️⃣ Distruzione
    if chunk_destroy_queue:
        coords = chunk_destroy_queue.pop(0)
        chunks[coords].unload()
        destroy(chunks[coords])
        del chunks[coords]
        print(f"🗑️ Chunk distrutto: {coords}")
        return


"""chunk_generation_queue = []

def update_chunks():
    global chunks, chunk_generation_queue

    player_chunk_x = int(player.position[0] // chunk_size)
    player_chunk_z = int(player.position[2] // chunk_size)

    active_chunks = set()

    # Calcola i chunk da mantenere attivi
    for dx in range(-render_distance, render_distance + 1):
        for dz in range(-render_distance, render_distance + 1):
            chunk_x = player_chunk_x + dx
            chunk_z = player_chunk_z + dz

            # ✅ Controllo limiti mondo
            if not (-world_bounds <= chunk_x <= world_bounds and -world_bounds <= chunk_z <= world_bounds):
                continue  # fuori dai limiti → salta

            chunk_coords = (chunk_x, chunk_z)
            active_chunks.add(chunk_coords)

            if chunk_coords not in chunks:
                # Nome file di salvataggio
                filename = f"chunksaves/chunk_({chunk_x*chunk_size},0,{chunk_z*chunk_size}).json"

                if os.path.exists(filename):
                    # Carica da file
                    chunks[chunk_coords] = load_chunk_from_file(
                        (chunk_x*chunk_size, 0, chunk_z*chunk_size)
                    )
                    chunks[chunk_coords].enable()
                    print(f"📂 Chunk caricato da file: {chunk_coords}")
                else:
                    # Aggiungi alla coda di generazione
                    chunk_generation_queue.append(chunk_coords)
                    print(f"🆕 Chunk aggiunto alla coda: {chunk_coords}")
            else:
                # Già in memoria → abilita
                chunks[chunk_coords].enable()


    # Salva e rimuovi i chunk fuori dal raggio
    for coords in list(chunks.keys()):
        if coords not in active_chunks:
            if chunks[coords].modified:
                save_chunk_to_file(chunks[coords])
                print(f"💾 Chunk salvato e rimosso dalla scena: {coords}")              
            
            #for child in chunks[coords].children:
            #    destroy(child)  # rimuove anche i Tree senza errori         
           
            chunks[coords].unload()

            # Rimuovi dal motore grafico
            destroy(chunks[coords])
            
            # Rimuovi dal dizionario
            del chunks[coords]
            print(f"💾 Chunk rimosso dalla scena: {coords}")      

            #print(f"💾 Chunk salvato e rimosso dalla scena: {coords}")


def process_chunk_queue():
    global chunk_generation_queue, chunks

    if chunk_generation_queue:
        chunk_coords = chunk_generation_queue.pop(0)
        chunk_x, chunk_z = chunk_coords
        origin = (chunk_x * chunk_size, 0, chunk_z * chunk_size)

        # Generazione del chunk in base al bioma
        biome = get_biome_type(origin[0], origin[2])
        config = terreni.get(biome, terreni["colline"])
        new_chunk = Chunk(origin=origin, **config)

        # Salva in memoria e su disco
        chunks[chunk_coords] = new_chunk
        save_chunk_to_file(new_chunk)
        print(f"✅ Chunk generato e salvato: {chunk_coords}")"""


#Creazione iniziale
chunks = {}
total_triangles = 0
for x in range(-render_distance, render_distance + 1):
    for z in range(-render_distance, render_distance + 1):
        origin = (x * chunk_size, 0, z * chunk_size)
        chunk_coords = (x, z)

        # Percorso del file salvato
        filename = f"chunksaves/chunk_({origin[0]},0,{origin[2]}).json"

        if os.path.exists(filename):
            # Carica chunk da file
            chunks[chunk_coords] = load_chunk_from_file(origin)
            print(f"📂 Chunk iniziale caricato da file: {chunk_coords}")
        else:
            # Genera nuovo chunk e salvalo
            biome = get_biome_type(origin[0], origin[2])
            #config = terreni.get(biome, terreni["colline"])
            config = TERRENI.get(biome, TERRENI["colline"])
            chunks[chunk_coords] = Chunk(origin=origin, **config)
            save_chunk_to_file(chunks[chunk_coords])
            print(f"🆕 Chunk iniziale generato: {chunk_coords}")

        chunk_generati_x_z.append(chunk_coords)


invoke(lambda: setattr(player, 'enabled', True), delay=2)


def save_load_current_chunk():
    # --- TEST ---
    # 1. Creazione chunk di prova
    chunk_x, chunk_z = get_chunk_coords(player.position)
    chunk_originale = chunks[(chunk_x,chunk_z)]
    # 2. Salvataggio
    save_chunk_to_file(chunk_originale)

    # 3. Caricamento
    chunk_caricato = load_chunk_from_file((chunk_x*chunk_size,0,chunk_z*chunk_size))
    chunk_caricato.position = (0,20,0)

    # 4. Verifica
    print("Origin originale:", chunk_originale.origin)
    print("Origin caricato :", chunk_caricato.origin)
    print("Numero alberi   :", len(chunk_caricato.alberi))
    print("Numero animali  :", len(chunk_caricato.animali))

        



highlight = Entity(
    model='cube',
    texture= 'highlight.png',
    color=color.rgba(0, 200, 255, 100),
    scale=1.01,
    visible=False
)

current_chunk = get_chunk_coords(player.position)

def aggiorna_blocco():
    global blocco_selezionato, selected_block_type
    #blocco_selezionato = cubi[indice]
    blocco_selezionato = CUBI[indice]
    selected_block_type = indice
    
    nome_blocco = blocco_selezionato['nome']
    path_texture = f'assets/{nome_blocco}.png'
    from os.path import exists
    bottone.texture = path_texture if exists(path_texture) else 'assets/default.png'
    testo_blocco.text = blocco_selezionato['nome']

def input(key):
    global selected_block_type,indice, blocco_selezionato,player, free_camera,light_on,  render_distance, BIOME_SCALE, modalita_creativa, hud_attivo, mini_map_on,world_map_show, mappa_mondo,map_entity, map_file
    
    if key == 'h':
        if player.enabled:
            # 🎮 FirstPersonControl attivo
            hit_info = raycast(camera.world_position + camera.forward * 0.5, camera.forward, distance=10, ignore=[player])
        else:           
            if mouse.hovered_entity:
                origin = free_camera.world_position
                direction = (mouse.world_point - origin).normalized()

                hit_info = raycast(origin, direction, distance=100)
            
        
              
        if hit_info.hit and isinstance(hit_info.entity, Vegetazione):
            veg = hit_info.entity

            if veg and veg.parent:
                current_chunk = veg.parent
                #print(f"🌿 Vegetazione distrutta nel chunk: {current_chunk}")
                destroy(veg)

                # Rimuovi dalla lista del chunk se presente
                if hasattr(current_chunk, 'vegetazione') and veg in current_chunk.vegetazione:
                    current_chunk.vegetazione.remove(veg)
            #else:
                #print("⚠️ Il fiore non ha più un parent valido o è già stato distrutto!")
        

    if key == 'tab':
        if player.enabled:         
            mouse.locked = False
            player_model.visible = True
            player_model.position = player.position 
            player_model.rotation = player.rotation
            if player.weapon:
                player.weapon.visible = False
            player.enabled = False       
            free_camera.enabled = True          
            free_camera.position = player.position
            #free_camera.rotation = player.camera_pivot.rotation
            free_camera.rotation = player.camera_pivot.world_rotation
        else:                     
            free_camera.enabled = False
            player_model.visible = False
            player.enabled = True
            player.weapon.visible = True
            if not hasattr(player, 'collider') or player.collider is None:
                player.collider = BoxCollider(player, size=Vec3(1,2,1))
            #player.collider = BoxCollider(player, size=Vec3(1,2,1))
            player.gravity = 0.5
            mouse.locked = True
 

    """if key == 'e':
        indice = (indice + 1) % len(cubi)
        aggiorna_blocco()
    elif key == 'q':
        indice = (indice - 1) % len(cubi)
        aggiorna_blocco()"""
    
    if key == 'e':
        indice = (indice + 1) % len(CUBI)
        aggiorna_blocco()
    elif key == 'q':
        indice = (indice - 1) % len(CUBI)
        aggiorna_blocco()

    if key == 'f':
        window.fullscreen = not window.fullscreen
    if key == 'escape':
        application.quit()

    
    
    elif key == 'right mouse down' and modalita_creativa:
        if mouse.hovered_entity and isinstance(mouse.hovered_entity, Chunk):
            if mouse.world_point and mouse.normal:
                hit = mouse.world_point - mouse.normal * 0.5
                block_pos = (floor(hit.x), floor(hit.y), floor(hit.z))
                for chunk in chunks.values():
                    if block_pos in chunk.blocks:
                        chunk.remove_block(block_pos)
                        audio_manager.play_sound('place_block')
                        break
    elif key == 'left mouse down' and modalita_creativa:
        if mouse.hovered_entity and isinstance(mouse.hovered_entity, Chunk):
            if mouse.world_point and mouse.normal:
                place_pos = mouse.world_point + mouse.normal * 0.5
                block_pos = (floor(place_pos.x), floor(place_pos.y), floor(place_pos.z))
                for chunk in chunks.values():
                    if (chunk.origin[0] <= block_pos[0] < chunk.origin[0] + chunk_size and
                        chunk.origin[1] <= block_pos[1] < chunk.origin[1] + chunk_size and
                        chunk.origin[2] <= block_pos[2] < chunk.origin[2] + chunk_size):
                        
                        chunk.blocks[block_pos] = selected_block_type
                        audio_manager.play_sound('place_block')
                        chunk.build_mesh()
                        break
    #elif key == 'k':      
    #    panel.enabled = not panel.enabled
    #elif key == 'l':      
    #    load_menu.enabled = not load_menu.enabled
    elif key == 'f1':
        light_on = not light_on
        light.shadows = light_on  
        light.enabled = light_on    
        print(f"Luce {'attiva' if light_on else 'spenta'}")
    elif key == 'f2':
        global highligh_on
        highligh_on = not highligh_on
        if highligh_on and modalita_creativa: 
            highlight.enabled = True
        else:
            highlight.enabled = False
    elif key == 'f3':
        mini_map_on = not mini_map_on
        minimap.enabled = mini_map_on
    elif key == 'f4':
        hud_attivo = not hud_attivo          
    elif key == 'f6':
        player.position += Vec3(0,16,0) 
    elif key == 'f7':
        save_load_current_chunk()    
    elif key == 'f8':
        if map_entity is None:
            map_file = os.path.join(MAPS_DIR, f"mappa_{int(time.time())}.png")
            mappa.genera_mappa_png()
            mappa.stampa_mappa_chunk()

            img = Image.open(map_file)
            w, h = img.size
            aspect_ratio = w / h

            # 🔹 Calcolo dinamico per stare sempre nello schermo
            max_display_height = 0.8   # 80% dell'altezza disponibile
            max_display_width = 0.8    # 80% della larghezza disponibile

            display_height = min(max_display_height, max_display_width / aspect_ratio)
            display_width = display_height * aspect_ratio

            map_entity = Entity(
                parent=camera.ui,
                model='quad',
                texture=load_texture(map_file),
                scale=(display_width, display_height),
                position=(0, 0),
                enabled=True
            )

        else:
            map_entity.enabled = not map_entity.enabled

            if map_entity.enabled:
                map_file = os.path.join(MAPS_DIR, f"mappa_{int(time.time())}.png")
                mappa.genera_mappa_png()

                map_entity.texture = load_texture(map_file)

                img = Image.open(map_file)
                w, h = img.size
                aspect_ratio = w / h

                max_display_height = 0.8
                max_display_width = 0.8

                display_height = min(max_display_height, max_display_width / aspect_ratio)
                display_width = display_height * aspect_ratio

                map_entity.scale = (display_width, display_height)
    elif key == 'f9': 
        from collections import Counter
        print("Entità attive: ")
        attive = [e for e in scene.entities if e.enabled]
        print(Counter(type(e).__name__ for e in attive))

        for e in attive:
            if not hasattr(e, 'parent') or e.parent is None:
                print("Orfano:", e, type(e).__name__)
            elif not isinstance(e.parent, Chunk) and not isinstance(e, Chunk):
                print("Fuori chunk:", e, type(e).__name__, "parent:", type(e.parent).__name__)
    elif key == '+':      
        render_distance = clamp(render_distance + 1, 1, MAX_render_distance)
        print(f"🔄 Nuova render_distance: {render_distance}")
        update_chunks()
    elif key == '-':     
        render_distance = clamp(render_distance - 1, 1, MAX_render_distance)
        print(f"🔄 Nuova render_distance: {render_distance}")
        update_chunks()
    elif held_keys['up arrow']:        
        BIOME_SCALE += 5
        BIOME_SCALE = max(min(BIOME_SCALE, 500), 1)
    elif held_keys['down arrow']:
        BIOME_SCALE -= 5
        BIOME_SCALE = max(min(BIOME_SCALE, 500), 1)
    elif key == 'm':     
        modalita_creativa = not modalita_creativa
        bottone.enabled = not bottone.enabled
        testo_blocco.enabled = not testo_blocco.enabled
        highlight.enabled = modalita_creativa
    elif key == 'i':
        world_map_show = not world_map_show
        print(f"chunk generati: {len(chunk_generati_x_z)}  {chunk_generati_x_z}")  
        if len(chunk_generati_x_z) != len(set(chunk_generati_x_z)):
            print("C'è almeno un doppione!")
        else:
            print("Tutti unici.")               

def get_blocco_sotto(player, chunk_size):
    pos_vec = player.position + Vec3(0, 0.1, 0)
    blocco_sotto = (floor(pos_vec.x),floor(pos_vec.y-1),floor(pos_vec.z))
    chunk_coords = (blocco_sotto[0] // chunk_size,blocco_sotto[2] // chunk_size)
    chunk = chunks.get(chunk_coords)
    if chunk and blocco_sotto in chunk.blocks:
        tipo = chunk.blocks[blocco_sotto]
        if tipo is not None:
            #return cubi[tipo]['nome']
            return CUBI[tipo]['nome']
    return None

def is_player_stuck(player, previous_y, tempo_senza_terreno):
    hit = raycast(player.position + Vec3(0, 0.1, 0), Vec3(0, -1, 0), distance=0.2, ignore=[player])
    if not hit.hit:
        tempo_senza_terreno += time.dt
    else:
        tempo_senza_terreno = 0

    movimento_verticale = abs(player.y - previous_y)
    stuck = tempo_senza_terreno > 0.5 and movimento_verticale < 0.01
    return stuck, tempo_senza_terreno


tempo_senza_terreno = 0
previous_y = 0

def update():
    global current_chunk, world_bounds,  tempo_senza_terreno, previous_y, chunks_esplorati #selected_block_pos
    
    # Calcolo FPS
    fps = int(1 / time.dt)
    #chunk_visibili = [c for c in chunks.values() if c.enabled]

    

    #guarda se il player è incastrato
    """stuck, tempo_senza_terreno = is_player_stuck(player, previous_y, tempo_senza_terreno)
    if stuck:
        print("🚨 Player incastrato! Teletrasporto in corso...")
        player.position += Vec3(0,1.1,0)
        tempo_senza_terreno = 0  # resetta il timer dopo il teletrasporto
    previous_y = player.y"""


    #------------ Guarda se player si muo ve e fa un suono---------
    global previous_pos, last_step_time
    current_pos = player.position
    movement = current_pos - previous_pos

    if movement.length() > 0.01:
        now = time.time()
        
        if now - last_step_time > step_interval:
            nome_blocco = get_blocco_sotto(player, chunk_size)
            if nome_blocco in audio_manager.mappa_blocchi_suoni:
                nome_suono = audio_manager.mappa_blocchi_suoni[nome_blocco]
                audio_manager.play_sound(nome_suono)
                last_step_time = now         

    previous_pos = current_pos
    #------------------------------------------

    # Ottieni posizione attuale del giocatore
    player_pos = player.position
    chunk_x, chunk_z = get_chunk_coords(player_pos)

    """global prev_count
    current_entities = [e for e in scene.entities if e.enabled]
    if len(current_entities) > prev_count:
        print(f"⚠️ Nuove entità attive: {len(current_entities) - prev_count}")
        for e in current_entities[prev_count:]:
            print(f"➕ {e} | model: {e.model} | parent: {e.parent} | time: {time.dt}")
        prev_count = len(current_entities)"""

    if hud_attivo:
        visibili = [coords for coords, c in chunks.items() if c.enabled]
        info_hud.text = (
            f"FPS: {fps}\n"
            f"Chunk visibili: {len( [c for c in chunks.values() if c.enabled])}\n"            
            f"Entità attive: {len([e for e in scene.entities if e.enabled])}\n"
            f"Chunk visibili {len(visibili)}): {visibili}\n"
            f"Blocco selezionato: {selected_block_type}\n"
            f"Posizione: ({player.position.x:.2f}, {player.position.y:.2f}, {player.position.z:.2f})\n"
            f"Chunk: X={chunk_x}, Z={chunk_z}\n"
            f"Lights = {light_on} qualità: {light.shadow_map_resolution} \n"
            f"Minimap = {mini_map_on}\n"
            f"Render distance= {render_distance}\n"
            f"Bioma scala = {BIOME_SCALE}\n"
            f"Modalità creativa = {modalita_creativa}\n"
            f"Animali_attivi = {len([e for e in scene.entities if isinstance(e, Animal) and e.enabled])} %unità = {PERC_ANIMALS_SPAWS*100} \n"
            f"Alberi_attivi = {len([e for e in scene.entities if isinstance(e, Tree) and e.enabled])}  %unità = {PERC_TREES_SPAWS*100} \n"
            f"Vegetazioni = {len([e for e in scene.entities if isinstance(e, VegetazioneChunk) and e.enabled])} \n"
            f"Chunks esplorati = {chunks_esplorati} mondo esplorato = {round((chunks_esplorati / total_chunks) * 100, 1)} \n"
        )
    else:
        info_hud.text =  (f"FPS: {fps}\n")
  
    # Controllo confini e respingimento
    if abs(chunk_x) > world_bounds or abs(chunk_z) > world_bounds:
        center = Vec3(0, player_pos.y, 0)
        direction = (player_pos - center).normalized()
        player.position -= direction * time.dt * 25

        print("🚫 Confine superato! Giocatore respinto.")
 
    
    # Aggiorna chunk se necessario
    new_chunk = (chunk_x, chunk_z)
    if new_chunk != current_chunk:
        update_chunks()        
        current_chunk = new_chunk
          
        if new_chunk not in chunks_visitati:
            chunks_visitati.add(new_chunk)
            chunks_esplorati += 1
            mappa.aggiorna_chunk(chunk_x, chunk_z)

    #start = time.perf_counter()
    #process_chunk_queue()
    process_chunk_queues()
    #print(f"⏱ Tempo generazione chunk: {time.perf_counter() - start:.4f} sec")


    # Evidenziazione blocco sotto il cursore
    if highligh_on and modalita_creativa:
        origin = camera.world_position + camera.forward * 0.5
        hit_info = raycast(origin, camera.forward, distance=20, ignore=[player])

        if hit_info.hit:
            normal = hit_info.normal
            hit_point = hit_info.point

            block_pos = (floor(hit_point.x - normal.x * 0.5),floor(hit_point.y - normal.y * 0.5),floor(hit_point.z - normal.z * 0.5))

            # Cerca il blocco nei chunk
            for chunk in chunks.values():
                if block_pos in chunk.blocks:
                    # Posiziona l'highlight al centro del blocco
                    highlight.position = Vec3(block_pos[0] + 0.5,block_pos[1] + 0.5,block_pos[2] + 0.5)
                    highlight.visible = True
                    #selected_block_pos = block_pos  # <-- aggiunto
                    break
            else:
                highlight.visible = False
        else:
            highlight.visible = False
            #selected_block_pos = None  # <-- reset se non c'è blocco

    # Simula un sole che ruota attorno al mondo
    if light_on:
        angle = time.time() * 0.15  # Velocità di rotazione
        light.look_at(Vec3(sin(angle), -1, cos(angle)))

        shadow_bounds.position = player.position
        light.update_bounds(shadow_bounds)

    #print(time.dt)
#window.vsync = False

app.run()
