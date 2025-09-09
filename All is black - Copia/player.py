from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from animal import Animal
from tree import Tree

import time as pytime

class Player(FirstPersonController):
    def __init__(self, hud,  audio_manager, items_list, position = (0,0,0) ,**kwargs):
        super().__init__(**kwargs)

        self.audio_Manager = audio_manager
        self.position = Vec3(position)
        self.collider = BoxCollider(self, size=Vec3(0.9,1.9,0.9))
        self.gravity = 0.5
        self.jump_height = 2

        self.attaccando = False
        self.cooldown_time_attack = 0.2
        self.pickDistance = 2.5
        self.pickAngle = 45
        self.items_list = items_list
        self.inventory = []

        self.weapon = Entity(
            parent = camera,
            position= (0.5,-0.75,1),
            rotation= (0, 45, 0),
            model='assets/models/items/axe.obj',
            texture = 'assets/models/items/axe.png',
            scale=0.25
        )

        self.step_offset = 0.05  # margine di sollevamento in metri
        self.blocked_frames = 0


        self.max_health = 100
        self.health = 100   
        self.score = 0
        self.level = 1
        self.exp = 0
        self.hud = hud
        self.update_hud()

    def input(self, key):
        super().input(key)

        if key == 'left mouse down':  # oppure un altro tasto come 'e' o 'space'
           self.attacca()

        if key== 'p':           
            for item in self.items_list:
                if self.can_pick(item):
                    self.collect(item)
                    break

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        self.update_hud()

        if self.health <= 0:
           self.die()

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
        self.update_hud()


    def add_score(self, amount):
        self.score += amount
        self.update_hud()

    def add_exp(self, amount):
        self.exp += amount
        self.update_hud()

    def add_level(self, amount):
        self.level += amount
        self.update_hud()

    def die(self):
        print("Il player è morto!")
        self.enabled = False
        death_text = Text(text="GAME OVER",origin=(0,0),scale=2,color=color.red,parent=camera.ui)   
        #self.audio_Manager.play_sound('death')     
        invoke(application.quit, delay=3)  # esempio: chiude il gioco


    def update_hud(self):
        """Aggiorna la barra e il testo della vita"""
        self.hud.update_health(self.health, self.max_health)
        self.hud.update_score(self.score)
        self.hud.update_exp(self.exp)
        self.hud.update_level(self.level)


    def update(self):
        #start = pytime.time()

        prev_pos = self.position
        super().update()

        #after_super = pytime.time()

       # Controllo blocco solo se sto cercando di muovermi
        if self.is_moving():
            if self.position == prev_pos:
                self.blocked_frames += 1
            else:
                self.blocked_frames = 0

            if self.blocked_frames >= 2:
                self.y += self.step_offset
                self.blocked_frames = 0
        else:
            self.blocked_frames = 0  # reset se fermo

        # Se non ci siamo mossi (bloccati), prova a sollevare leggermente
        #if self.position == prev_pos:
        #    self.y += self.step_offset
            #super().update()

        # Effetto camminata sull'arma old
        """if self.is_moving() and not self.attaccando:
            t = time.time()
            self.weapon.position.y = -0.75 + math.sin(t * 8) * 0.05  # su/giù
            self.weapon.position.x = 0.5 + math.sin(t * 4) * 0.03    # oscillazione laterale
            self.weapon.rotation_z = math.sin(t * 6) * 2             # leggera rotazione
        elif not self.attaccando:
            # Reset posizione e rotazione quando fermo
            self.weapon.position = Vec3(0.5, -0.75, 1)
            self.weapon.rotation_z = 0"""

        if self.is_moving() and not self.attaccando:
            t = time.time()
            s1 = math.sin(t * 8)
            s2 = math.sin(t * 4)
            s3 = math.sin(t * 6)

            self.weapon.position = Vec3(
                0.5 + s2 * 0.03,
                -0.75 + s1 * 0.05,
                1
            )
            self.weapon.rotation_z = s3 * 2
        elif not self.attaccando:
            self.weapon.position = Vec3(0.5, -0.75, 1)
            self.weapon.rotation_z = 0

        #end = pytime.time()
        #print(f"super.update: {(after_super-start)*1000:.2f} ms | totale: {(end-start)*1000:.2f} ms")

    def can_pick(self, item):
        # Controllo distanza
        if distance(self.position, item.position) > self.pickDistance:
            return False

        # Direzione del player (in avanti)
        forward_vector = self.forward
        forward_vector.y = 0  # ignora differenze in altezza
        forward_vector = forward_vector.normalized()

        # Vettore verso l’oggetto
        to_item = item.position - self.position
        to_item.y = 0
        to_item = to_item.normalized()

        # Calcola angolo tra i due vettori
        angle = math.degrees(math.acos(clamp(forward_vector.dot(to_item), -1, 1)))

        return angle <= self.pickAngle and getattr(item, "pickable", False)

    def collect(self, item):      
        self.audio_Manager.play_sound('pick_up_item')
         # Suono ritardato (es. dopo 0.4 secondi)
        invoke(self.audio_Manager.play_sound, 'pop_item', delay=0.4)
        
        self.inventory.append(item)
        self.items_list.remove(item)

         # Animazione: scala verso zero in 0.3 secondi
        item.animate_scale(Vec3(0, 0, 0), duration=0.3, curve=curve.in_expo)

        # Distruggi l'oggetto dopo l'animazione
        invoke(destroy, item, delay=0.3)

        #destroy(item)  # rimuove l'oggetto dal mondo
        print(f"Raccolto: {item} | Inventario: {len(self.inventory)} oggetti")

    def attacca(self):
        if self.attaccando:
            return  # evita spam di attacchi

        self.attaccando = True

        # Animazione semplice dell'arma (oscillazione)
        self.weapon.animate_rotation((10, 45, -80), duration=0.075, curve=curve.linear)
        invoke(self.reset_weapon, delay=self.cooldown_time_attack)

        hit_info = raycast(camera.world_position, camera.forward, distance=2, ignore=[self])
        if hit_info.hit:
            #hit_info.entity.color = color.red
            print(f"Colpito: {hit_info.entity}, punto: {hit_info.point}")
            if isinstance(hit_info.entity,Tree):
                hit_info.entity.on_hit()
            elif isinstance(hit_info.entity, Animal):
                hit_info.entity.prendi_danno(10, attaccante=self)
        else: 
            self.audio_Manager.play_sound('axe_miss')
            print("Non hai colpito nulla!")
    
    def reset_weapon(self):
        self.weapon.rotation = (10, 45, 0)
        self.attaccando = False

    def is_moving(self):
        return held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']