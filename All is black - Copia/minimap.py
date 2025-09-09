from ursina import *
import math
import time
from animal import Animal
from npc import NPC
from tree import Tree
from vegetation import Vegetazione

class MiniMap(Entity):
    MARKER_TEXTURES = {
        Tree: 'assets/flowericon.png',
        Animal: lambda ent: f'assets/{ent.nome.lower()}icon.png',
        NPC: 'assets/npcicon.png'
    }

    def __init__(self, player, radius=20, scale=0.085, position=(0.7, 0.3), scan_interval=0.5, **kwargs):
        super().__init__(parent=camera.ui, position=position, scale=2, **kwargs)
        self.player = player
        self.radius = radius
        self.scale = scale
        self.scan_interval = scan_interval
        self.last_scan_time = time.time()
        self.tracked = []
        self.markers = {}

        self.radar = Entity(parent=self, model='cube', texture='assets/radar.png', scale=4.75, z=100)
        self.player_marker = Entity(parent=self, model='circle', color=color.azure, scale=0.15, z=1, position=(0, 0, 0.02))

    def scan_entities(self):
        new_tracked = [
            ent for ent in scene.entities
            if ent != self.player
            and ent not in self.markers.values()
            and getattr(ent, "traceable", False)
        ]

        # Disabilita marker di entità non più presenti
        for ent in list(self.markers.keys()):
            if ent not in new_tracked or not ent.enabled or ent not in scene.entities:
                self.markers[ent].enabled = False
                del self.markers[ent]

        self.tracked = new_tracked

    def update(self):
        current_time = time.time()
        if current_time - self.last_scan_time > self.scan_interval:
            self.scan_entities()
            self.last_scan_time = current_time

        # Calcola rotazione una sola volta
        forward = self.player.forward.normalized()
        angle_rad = math.radians(math.degrees(math.atan2(forward.x, forward.z)))

        for ent in self.tracked:
            if not ent.enabled or ent not in scene.entities:
                if ent in self.markers:
                    self.markers[ent].enabled = False
                continue

            offset = ent.world_position - self.player.world_position
            offset_2d = Vec2(offset.x, offset.z)

            if offset_2d.length() > self.radius:
                if ent in self.markers:
                    self.markers[ent].enabled = False
                continue

            # Crea marker se non esiste
            if ent not in self.markers:
                texture = None
                for cls, tex in self.MARKER_TEXTURES.items():
                    if isinstance(ent, cls):
                        texture = tex(ent) if callable(tex) else tex
                        break
                if texture:
                    self.markers[ent] = Entity(parent=self, model='quad', texture=texture, scale=0.25, z=0.6)

            # Aggiorna posizione marker
            rotated = Vec2(
                offset_2d.x * math.cos(angle_rad) - offset_2d.y * math.sin(angle_rad),
                offset_2d.x * math.sin(angle_rad) + offset_2d.y * math.cos(angle_rad)
            ) * self.scale

            self.markers[ent].enabled = True
            self.markers[ent].position = Vec3(rotated.x, rotated.y, 0.01)


"""class MiniMap(Entity):
    def __init__(self, player, radius=20, scale=0.085, position=(0.7, 0.3), scan_interval=0.5, **kwargs):
        super().__init__(parent=camera.ui, position=position, scale=2, **kwargs)
        self.player = player
        self.radius = radius
        self.scale = scale
        self.scan_interval = scan_interval
        self.last_scan_time = time.time()
        self.tracked = []
        self.markers = {}

        self.radar = Entity(parent=self, model='cube',texture='assets/radar.png', scale=4.75,z=100)
        

        self.player_marker = Entity(
            parent=self,
            model='circle',
            color=color.azure,
            scale=0.15,
            z=1           
        )
        self.player_marker.position = Vec3(0, 0, 0.02)

    def scan_entities(self):
        new_tracked = []
        for ent in scene.entities:
            # Escludi il giocatore, la vegetazione e i marker stessi
            if ent == self.player: 
                continue
            if ent in self.markers.values():  # Evita di tracciare i marker
                continue
            if getattr(ent, "traceable", False):  # 👈 controlla il tag           
                new_tracked.append(ent)

        # Rimuovi marker associati a entità non più presenti
        for ent in list(self.markers.keys()):
            #if ent not in new_tracked:
            if ent not in new_tracked or not ent.enabled or ent not in scene.entities:
                self.markers[ent].disable()
                del self.markers[ent]

        self.tracked = new_tracked

        

    def update(self):
        current_time = time.time()
        if current_time - self.last_scan_time > self.scan_interval:
            self.scan_entities()
            self.last_scan_time = current_time

        # Calcola l'angolo di rotazione del giocatore
        forward = self.player.forward.normalized()
        angle = math.degrees(math.atan2(forward.x, forward.z))

        for ent in self.tracked:
            #if not ent.enabled:
            if not ent.enabled or ent not in scene.entities:
                if ent in self.markers:
                    self.markers[ent].enabled = False
                continue

                    
            offset = ent.world_position - self.player.world_position
            offset_2d = Vec2(offset.x, offset.z)

            # Escludi entità fuori dal raggio
            if offset_2d.length() > self.radius:
                if ent in self.markers:
                    self.markers[ent].enabled = False
                continue

            # Crea un marker se non esiste
            if ent not in self.markers:
                if isinstance(ent, Tree):                
                    marker_texture ='assets/flowericon.png'
                elif isinstance(ent, Animal):                
                    #print(f"nome animale: {ent.nome}")
                    marker_texture =f'assets/{ent.nome.lower()}icon.png'                    
                elif isinstance(ent, NPC):                  
                    marker_texture ='assets/npcicon.png'
                else:
                    marker_color = color.white
                           
                marker = Entity(parent=self, model='quad',texture= marker_texture, scale=0.25, z=0.6)
                self.markers[ent] = marker

            # Ruota e posiziona il marker sulla minimappa
            radians = math.radians(angle)
            rotated = Vec2(
                offset_2d.x * math.cos(radians) - offset_2d.y * math.sin(radians),
                offset_2d.x * math.sin(radians) + offset_2d.y * math.cos(radians)
            ) * self.scale

            self.markers[ent].enabled = True
            self.markers[ent].position = Vec3(rotated.x, rotated.y, 0.01)"""
